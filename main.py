import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import os
import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user
from flask_login import logout_user, login_required
from forms import RegistrationForm, LoginForm, receipt_upload, user_preference
from forms import button_for_script, button1_for_script, keyword, Trytest, Select_recipe, receipt_upload_adv
from api_keys import APIKEY, OCRKEY

app = Flask(__name__)

app.config["SECRET_KEY"] = "enter-a-hard-to-guess-string"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # To change
db = SQLAlchemy(app)  # To change
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(60), nullable=False)
    lname = db.Column(db.String(60), nullable=False)
    uname = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    receipts = db.relationship("Receipts", backref="op", lazy=True)
    items = db.relationship("Items", backref="opp", lazy=True)
    # num_of_items = db.Column(db.Integer, default=5)

    def __repr__(self):
        return f"User(id: '{self.id}', fname: '{self.fname}', " +\
               f" lname: '{self.lname}', uname: '{self.uname}')" +\
               f" password: '{self.password}', email: '{self.email}')"


class Receipts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    grain = db.Column(db.Integer, default=0)
    milk = db.Column(db.Integer, default=0)
    proteins = db.Column(db.Integer, default=0)
    greens = db.Column(db.Integer, default=0)
    fruits = db.Column(db.Integer, default=0)
    drinks = db.Column(db.Integer, default=0)
    misc = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Receipts(id: '{self.id}', grain: '{self.grain}', " +\
               f" milk: '{self.milk}', " +\
               f" proteins: '{self.proteins}', " +\
               f" greens: '{self.greens}', " +\
               f" fruits: '{self.fruits}', " +\
               f" drinks: '{self.drinks}', " +\
               f" misc: '{self.misc}', " +\
               f" date_created: '{self.date_created}', " +\
               f" op: '{self.user_id}')"


class Items(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, default=0)
    item = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Items(id: '{self.id}', session_id: '{self.session_id}', " +\
               f" item: '{self.item}', " +\
               f" date_created: '{self.date_created}', " +\
               f" user_id: '{self.user_id}')"




###########
# routes
###########


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if current_user.is_authenticated:
        current_id = current_user.id
        my_user = User.query.filter_by(id=current_id).first()
        items = get_items(0)
        popular = get_popular_items(5) #User.num_of_items)
        form = button_for_script()
        form1 = button1_for_script()

        if form.validate_on_submit():
            add_item(form)
            # items = get_items()
            return redirect(url_for("index"))
            # return render_template("index.html", form=form, form1=form1,
            #                         items=items, popular=popular)

        if form1.validate_on_submit():
            attribute_session_id()
            # items = get_items()
            # popular = get_popular_items(5)
            return redirect(url_for("index"))
            # return render_template("index.html", form=form, form1=form1,
            #                         items=items, popular=popular)

        return render_template("index.html", form=form,
                               form1=form1, items=items, popular=popular)
    else:
        return redirect(url_for("login"))


@app.route("/upload-receipt")   # Am on it
def manual_receipt():
    if current_user.is_authenticated:
        form = receipt_upload()
        if form.validate_on_submit():
           return true #placeholder
        return render_template("upload-receipt.html", form=form)
    else:
        return redirect(url_for("login"))


@app.route("/my-lists", methods=["GET", "POST"])
def my_lists():
    if current_user.is_authenticated:
        form = Select_recipe()

        df = pd.read_sql(Items.query.statement, db.session.bind)
        nd_df = df[df["user_id"] == current_user.id]
        nd_df = nd_df.drop_duplicates(subset='session_id', keep="last")
        nd_df = nd_df.sort_values(by='session_id', ascending=False)
        nd_df = nd_df.head().reset_index(drop=True)
        for i in range(0, 4):
            nd_df["date_created"][i] = str(nd_df["date_created"][i])[
                :10] + " at " + str(nd_df["date_created"][i])[11:19]
        items = get_items(0)

        choices = [(0, "current list"),
                   (1, "list from the " + str(nd_df["date_created"][0])),
                   (2, "list from the " + str(nd_df["date_created"][1])),
                   (3, "list from the " + str(nd_df["date_created"][2])),
                   (4, "list from the " + str(nd_df["date_created"][3]))]
        form.recipe_chosen.choices = choices

        if form.validate_on_submit():
            if form.recipe_chosen.data == 0:
                items = get_items(0)
            else:
                items = get_items(nd_df["session_id"][form.recipe_chosen.data - 1])

        return render_template("my_lists.html", items=items, form=form)
    else:
        return redirect(url_for("login"))


@app.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete(item_id):
    item = Items.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))

@app.route("/scan-receipt", methods=["POST", "GET"])
def receipt():
    if current_user.is_authenticated:
            #for testing purposes
        form = receipt_upload_adv(request.form)
        assets_dir = "static"
        filename = "receipt.jpg"
        path = os.path.join(assets_dir, filename) 
        

        payload = {'isOverlayRequired': False,
               'apikey': "498f0b56fb88957",
               'language': "ger",
               }
        with open(path, 'rb') as f:
            response = requests.post('https://api.ocr.space/parse/image',
                          files={path: f},
                          data=payload,
                          )
        
        print(response.content)
        response = response.content

        #cleaning up result

            #classify it

            #print Table so i can check

            #add to (previous bought) list

        if form.validate_on_submit():
            
            #get picture
            
            assets_dir = "static"
            filename = "receipt.jpg"
            path = os.path.join(assets_dir, filename) 
            form.receipt_picture.data.save(path)
            
            
            #API Call
            payload = {'isOverlayRequired': False,
               'apikey': "498f0b56fb88957",
               'language': "ger",
               }
            with open(path, 'rb') as f:
                response = requests.post('https://api.ocr.space/parse/image',
                          files={path: f},
                          data=payload,
                          )
            response = response.content
        
            
            #cleaning up result

            #classify it

            #print Table so i can check

            #add to (previous bought) list
        return render_template("scan-receipt.html", form=form)  
    else:
        return redirect(url_for("login"))

"""
Advanced functionalities

@app.route("/Analytics")
def analytics():
    if current_user.is_authenticated:
        # The fancy expense report
    else:
        return redirect(url_for("login"))






@app.route("/suggested-recipe", methods=["GET", "POST"])
def sugrec():
    if current_user.is_authenticated:
        # Recipe from picture
        form_picture = food_upload()
        form = Trytest()
        # this also returns nutritional info
        if form_picture.validate_on_submit():
            df = get_recipe_id_from_picture(form_picture.food_picture.data)
            choices = []
            for i in range(0, len(df)):
                choices.append((i, df["name"][i]))
            return render_template("suggested_recipe0.html",
                                   form_picture=form_picture, form=form,
                                   choices=choices)
        if form.validate_on_submit():
            df = get_recipe_id_from_picture(form_picture.food_picture.data)
            n = form.number.data - 1
            add_items_from_list(get_recipe_info(df["id"][n]),
                                len(get_recipe_info(df["id"][n])))
        return render_template("suggested_recipe.html", form=form,
                               form_picture=form_picture)
    else:
        return redirect(url_for("login"))
"""


@app.route("/find-recipe", methods=["GET", "POST"])
def findrec():
    if current_user.is_authenticated:
        # Find recipe from keyword
        form_diet = keyword()
        form2 = Trytest()
        if form_diet.validate_on_submit():
            id_df = get_recipe_id(form_diet.query.data, form_diet.diet.data,
                                  form_diet.excludeIngredients.data,
                                  form_diet.intolerances.data,
                                  10)
            choices = [(1, id_df["name"][0]),
                       (2, id_df["name"][1]),
                       (3, id_df["name"][2]),
                       (4, id_df["name"][3]),
                       (5, id_df["name"][4]),
                       (6, id_df["name"][5]),
                       (7, id_df["name"][6]),
                       (8, id_df["name"][7]),
                       (9, id_df["name"][8]),
                       (10, id_df["name"][9])]
            return render_template("find_recipe0.html",
                                   form_diet=form_diet, form2=form2,
                                   choices=choices)

        if form2.validate_on_submit():
            n = form2.number.data - 1
            id_df = get_recipe_id(form_diet.query.data, form_diet.diet.data,
                                  form_diet.excludeIngredients.data,
                                  form_diet.intolerances.data,
                                  10)  # idk why but this is necessary
            add_items_from_list(get_recipe_info(id_df["id"][n]),
                                len(get_recipe_info(id_df["id"][n])))
            return redirect(url_for("index"))
        return render_template("find_recipe.html",
                               form_diet=form_diet, form2=form2)
    else:
        return redirect(url_for("login"))


@app.route("/my-profile", methods=["GET", "POST"])
def my_profile():
    name, username, email = get_name()
    form = user_preference()
    if form.validate_on_submit():
        pref = form.preference.data

        current_id = current_user.id
        my_user = User.query.filter_by(id=current_id).first()

        my_user.num_of_items = pref

        db.session.commit()
        return redirect(url_for("index"))
    return render_template("my_profile.html",
                            name=name,
                            username=username,
                            email=email,
                            form=form)



@ app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        registration_worked = register_user(form)
        if registration_worked:
            flash("Registration successful. Please login")
            return redirect(url_for("login"))
    return render_template("register.html", form=form, User=User)


@ app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        if is_login_successful(form):
            flash("Login successful")
            return redirect(url_for("index"))
        else:
            if User.query.filter_by(email=form.email.data).count() > 0:
                flash("Login unsuccessful, please check your credentials"
                      "and try again")
            else:
                flash("Unknown credentials. Do you want to create an account?")
                return redirect(url_for("register"))
    return render_template("login.html", form=form, User=User)


@ app.route("/logout")
@ login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

############
# functions
############


def register_user(form_data):
    def email_already_taken(email):
        if User.query.filter_by(email=email).count() > 0:
            return True
        else:
            return False

    def uname_already_taken(uname):
        if User.query.filter_by(uname=uname).count() > 0:
            return True
        else:
            return False
    if email_already_taken(form_data.email.data):
        flash("That email is already taken!")
        return False
    if uname_already_taken(form_data.uname.data):
        flash("That username is already taken!")
        return False
    hashed_password = bcrypt.generate_password_hash(form_data.password.data)
    user = User(fname=form_data.fname.data,
                lname=form_data.lname.data,
                uname=form_data.uname.data,
                email=form_data.email.data,
                password=hashed_password)
    db.session.add(user)  # local sql databasr
    db.session.commit()  # local sql databasr
    return True


def is_login_successful(form_data):

    email = form_data.email.data
    password = form_data.password.data
    user = User.query.filter_by(email=email).first()
    if user is not None:
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return True
    else:
        return False


def get_name():
    current_id=current_user.id
    my_user=User.query.filter_by(id=current_id).first()
    if my_user is None:
        return False
    name=my_user.fname + " " + my_user.lname
    username=my_user.uname
    email=my_user.email
    return name, username, email


def add_item(form_data):
    product = Items(item=form_data.item.data,
                    date_created=datetime.datetime.now(),
                    user_id=current_user.id)
    db.session.add(product)
    db.session.commit()
    return product


def add_items_from_list(item_list, list_len):
    for i in range(0, list_len):
        product = Items(item=item_list[i],
                        date_created=datetime.datetime.now(),
                        user_id=current_user.id,
                        session_id=0)
        db.session.add(product)
        db.session.commit()


def get_items(session_id):
    df = pd.read_sql(Items.query.statement, db.session.bind)
    current_df = df[df["user_id"] == current_user.id]
    current_df = current_df[current_df["session_id"] == session_id]
    return current_df


def get_popular_items(num_of_items):
    df = pd.read_sql(Items.query.statement, db.session.bind)
    current_df = df[df["user_id"] == current_user.id]
    top_n_lst = current_df['item'].value_counts()[:num_of_items].index.tolist()
    img_lst=[]
    for i in top_n_lst:
        img_url=search_img(i)
        filename = i + ".jpg"
        filepath = save_img(img_url, "static/data/", filename)
        img_lst.append(filepath)
    data = {"item": top_n_lst,
            "path": img_lst}
    top_n_df = pd.DataFrame(data, columns = ["item", "path"])
    return top_n_df


def search_img(search_query):
    access_key = "KtozeG1fDJdYwiTtQRpDr0XVaSb_NyT_mKbBQ2gI1lg"
    url = "https://api.unsplash.com/search/photos/"
    parameter = {"client_id" : access_key,
                 "query" : search_query}
    r = requests.get(url, params=parameter)
    data=r.json()
    url_raw = data["results"][0]["urls"]["small"]
    return url_raw



def save_img(img_url, folder_prefix, filename):
    img = requests.get(img_url)
    file_path = os.path.join(folder_prefix, filename)
    with open(file_path, "wb") as file:
        file.write(img.content)
    return file_path



def attribute_session_id():
    num_of_nuls = Items.query.filter_by(user_id=current_user.id).filter_by(session_id=0).count()
    last_sid = Items.query.order_by(Items.session_id.desc()).first().session_id+1
    for i in range(0, num_of_nuls):
        list_of_null_sids = Items.query.filter_by(
            user_id=current_user.id).filter_by(session_id=0).first()
        setattr(list_of_null_sids, 'session_id', last_sid)
        db.session.commit()


def get_recipe_id(query, diet, excludeIngredients, intolerances, number):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
    querys = {"query": query, "diet": diet,
              "excludeIngredients": excludeIngredients,
              "intolerances": intolerances,
              "number": number}
    headers = {
        'x-rapidapi-key': APIKEY,  # still have to register
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querys)
    response = response.json()
    response
    recipe_ids = []
    recipe_names = []
    for i in range(0, number):
        recipe_ids.append(response["results"][i]["id"])
        recipe_names.append(response["results"][i]["title"])
    return pd.DataFrame({'id': recipe_ids, 'name': recipe_names},
                        columns=['id', 'name'])


def get_recipe_info(idn):
    idn = str(idn)
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/" + idn + "/information"
    headers = {
        'x-rapidapi-key': APIKEY,  # still have to register
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)

    ingredients = []
    for i in range(0, len(response["extendedIngredients"])):
        ingredients.append(response["extendedIngredients"][i]["originalString"])
    return ingredients


"""
def get_recipe_id_from_picture(food_picture):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/images/analyze"
    payload = food_picture
    headers = {
        'content-type': "multipart/form-data",
        'x-rapidapi-key': "9da2f73c89msh93d02299250d2d3p11c66djsnf01090a6a4b6",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    response = response.json()
    response
    recipe_ids = []
    recipe_names = []

    nutrition = {'values': [response["nutrition"]["calories"]["value"],
                            response["nutrition"]["fat"]["value"],
                            response["nutrition"]["protein"]["value"],
                            response["nutrition"]["carbs"]["value"]],
                 'unit': [response["nutrition"]["calories"]["unit"],
                          response["nutrition"]["fat"]["unit"],
                          response["nutrition"]["protein"]["unit"],
                          response["nutrition"]["carbs"]["unit"]]}

    food_nutrition = pd.DataFrame(nutrition, columns=['value', 'unit'])

    for i in range(0, len(response["recipes"])):
        recipe_ids.append(response["recipes"][i]["id"])
        recipe_names.append(response["recipes"][i]["title"])

    food_nutrition["id"] = recipe_ids
    food_nutrition["name"] = recipe_names

    return food_nutrition
"""


if __name__ == "__main__":
    app.run(debug=True)

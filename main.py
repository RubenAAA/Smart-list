from api_keys import *
from forms import Select_recipe, receipt_upload_adv, Select_element, Test
from forms import button_for_script, button1_for_script, keyword, Trytest
from forms import RegistrationForm, LoginForm, user_preference, pimage
from flask_login import logout_user, login_required
from flask_login import LoginManager, UserMixin, login_user, current_user
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, flash
from sys import platform
import requests
import datetime
import json
import os
from PIL import Image, ImageFile
import pandas as pd

app = Flask(__name__)

app.config["SECRET_KEY"] = "enter-a-hard-to-guess-string"
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # To change
db = SQLAlchemy(app)  # To change
bcrypt = Bcrypt(app)
ImageFile.LOAD_TRUNCATED_IMAGES = True
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
    items = db.relationship("Items", backref="opp", lazy=True)
    num_of_items = db.Column(db.Integer, default=5)
    profile_picture = db.Column(db.String(100), default="default")

    def __repr__(self):
        return f"User(id: '{self.id}', fname: '{self.fname}', " +\
               f" lname: '{self.lname}', uname: '{self.uname}')" +\
               f" password: '{self.password}', email: '{self.email}')"


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
        popular = get_popular_items(my_user.num_of_items)
        form = button_for_script()
        form1 = button1_for_script()

        if form.validate_on_submit():
            add_item(form)
            return redirect(url_for("index"))

        if form1.validate_on_submit():
            attribute_session_id()
            return redirect(url_for("index"))

        return render_template("index.html", form=form,
                               form1=form1, items=items, popular=popular)
    else:
        return redirect(url_for("login"))


@app.route("/upload-receipt", methods=["GET", "POST"])
def manual_receipt():

    if current_user.is_authenticated:

        form2 = receipt_upload_adv()
        form3 = Select_element()
        showform3 = True
        form3.element_chosen.choices = []
        liste_product = Test().product_list

        if form2.validate_on_submit():
            flash("This might take a few seconds")
            # get picture
            if platform == "linux" or platform == "linux2":
                assets_dirl = "/home/joel_treichler28/Smart-list/static/"  # yes it's ugly and not good practice
            else:
                assets_dirl = "static/"
            filenamel = form2.receipt_picture.name + ".jpg"
            pathl = assets_dirl + filenamel

            form2.receipt_picture.data.save(pathl)

            # compress picture
            picture = Image.open(pathl)
            picture.save(pathl,
                         "JPEG",
                         optimize=True,
                         quality=10)

            # API Call
            payload = {'isOverlayRequired': "false",
                       'apikey': OCR_KEY,
                       'language': "ger",
                       "isTable": "True",
                       "detectOrientation": "true",
                       }
            with open(pathl, 'rb') as f:
                response = requests.post('https://api.ocr.space/parse/image',
                                         files={pathl: f},
                                         data=payload,
                                         )

            # cleaning up result

            response = response.content.decode()
            response = json.loads(response)

            try:
                # cuts the json to the parts we need, it is now a list
                response = response["ParsedResults"][0]["TextOverlay"]["Lines"]

            except:
                flash("Error in Parsing the File try another one")
                return redirect(url_for("manual_receipt"))

            for i in response[3:]:  # starts at 3 because everything beforhand will be information about the shop
                i = i["LineText"]
                if i == "TOTAL" or i == "Total":  # stops it if no more items come
                    break
                if i == "Subtotal" or i == "SUBTOTAL" or i == "CHF" or i == "Aktion" or i == "AKTION" or i == "chf":  # ignores useless elements
                    continue
                try:
                    float(i)
                except ValueError:
                    liste_product.append(i)

            print(liste_product)

            # establish the choices for the list
            form_list = []
            c = 0
            for i in liste_product:
                form_list.append((c, i))
                c += 1
            form3.element_chosen.choices = [i for i in form_list]

            # delete picture
            if os.path.exists(pathl):
                os.remove(pathl)
            else:
                print("The file does not exist")

            showform3 = True

            # redirect(url_for("manual_receipt"))

        if form3.validate_on_submit():

            print(form3.element_chosen.data)
            iterator = int(form3.element_chosen.data)
            print(liste_product)
            # add to DB
            last_sid = Items.query.order_by(Items.session_id.desc()).first().session_id+1
            for li in liste_product[iterator:]:  # iterates starting with element chosen
                print(li)
                product = Items(item=li,  # add to  list
                                date_created=datetime.datetime.now(),
                                user_id=current_user.id,
                                session_id=last_sid)
                db.session.add(product)

            # commit
            db.session.commit()
            form3.element_chosen.choices = [(1, "")]
            flash("Items have been added to your current shopping list")
            liste_product = [""]
            return redirect(url_for("index"))

        return render_template("upload-receipt.html", form2=form2,
                               showform3=showform3, form3=form3)
    else:
        return redirect(url_for("login"))


@app.route("/my-lists", methods=["GET", "POST"])
def my_lists():
    if current_user.is_authenticated:
        form = Select_recipe()

        df = pd.read_sql(Items.query.statement, db.session.bind)
        nd_df = df[df["user_id"] == current_user.id]
        if nd_df.empty is False:
            nd_df = nd_df.drop_duplicates(subset='session_id', keep="last")
            nd_df = nd_df.sort_values(by='session_id', ascending=False)
            nd_df = nd_df.head().reset_index(drop=True)
            if len(nd_df.index) >= 5:
                for i in range(0, 4):
                    nd_df["date_created"][i] = str(nd_df["date_created"][i])[
                        :10] + " at " + str(nd_df["date_created"][i])[11:19]
                items = get_items(0)
                lll = 5
                choices = [(0, "current list"),
                           (1, "list from the " + str(nd_df["date_created"][0])),
                           (2, "list from the " + str(nd_df["date_created"][1])),
                           (3, "list from the " + str(nd_df["date_created"][2])),
                           (4, "list from the " + str(nd_df["date_created"][3]))]

            elif len(nd_df.index) == 4:
                for i in range(0, 3):
                    nd_df["date_created"][i] = str(nd_df["date_created"][i])[
                        :10] + " at " + str(nd_df["date_created"][i])[11:19]
                items = get_items(0)
                lll = 4
                choices = [(0, "current list"),
                           (1, "list from the " + str(nd_df["date_created"][0])),
                           (2, "list from the " + str(nd_df["date_created"][1])),
                           (3, "list from the " + str(nd_df["date_created"][2]))]

            elif len(nd_df.index) == 3:
                for i in range(0, 2):
                    nd_df["date_created"][i] = str(nd_df["date_created"][i])[
                        :10] + " at " + str(nd_df["date_created"][i])[11:19]
                items = get_items(0)
                lll = 3
                choices = [(0, "current list"),
                           (1, "list from the " + str(nd_df["date_created"][0])),
                           (2, "list from the " + str(nd_df["date_created"][1]))]

            elif len(nd_df.index) == 2:
                for i in range(0, 1):
                    nd_df["date_created"][i] = str(nd_df["date_created"][i])[
                        :10] + " at " + str(nd_df["date_created"][i])[11:19]
                items = get_items(0)
                lll = 2
                choices = [(0, "current list"),
                           (1, "list from the " + str(nd_df["date_created"][0]))]

            elif len(nd_df.index) == 1:
                items = get_items(0)
                lll = 1
                choices = [(0, "current list")]

            form.recipe_chosen.choices = choices

            if form.validate_on_submit():
                if form.recipe_chosen.data == 0:
                    items = get_items(0)
                else:
                    items = get_items(nd_df["session_id"][form.recipe_chosen.data - 1])

            return render_template("my_lists.html", items=items, form=form,
                                   lll=lll)
        else:
            lll = 0
            return render_template("my_lists.html", lll=lll)
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


@app.route("/analytics")
def analytics():
    if current_user.is_authenticated:
        return render_template("analytics.html")
    else:
        return redirect(url_for("login"))


@app.route("/find-recipe", methods=["GET", "POST"])
def findrec():
    if current_user.is_authenticated:
        form_diet = keyword()
        form2 = Trytest()
        choices = []
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
            return render_template("find_recipe.html",
                                   form_diet=form_diet, form2=form2,
                                   choices=choices)

        if form2.validate_on_submit():
            n = form2.number.data - 1
            id_df = get_recipe_id(form_diet.query.data, form_diet.diet.data,
                                  form_diet.excludeIngredients.data,
                                  form_diet.intolerances.data,
                                  10)
            add_items_from_list(get_recipe_info(id_df["id"][n]),
                                len(get_recipe_info(id_df["id"][n])))
            return redirect(url_for("index"))
        return render_template("find_recipe.html",
                               form_diet=form_diet, form2=form2,
                               choices=choices)
    else:
        return redirect(url_for("login"))


@app.route("/my-profile", methods=["GET", "POST"])
def my_profile():
    if current_user.is_authenticated:
        name, username, email = get_name()
        form = user_preference()
        form_img = pimage()
        if form.validate_on_submit():
            pref = form.preference.data

            current_id = current_user.id
            my_user = User.query.filter_by(id=current_id).first()

            my_user.num_of_items = pref

            db.session.commit()
            return redirect(url_for("index"))

        if form_img.validate_on_submit():
            form_img = form.pimage.data

            current_id = current_user.id
            my_user = User.query.filter_by(id=current_id).first()
            if platform == "linux" or platform == "linux2":  # linux
                # yes I know it's not the good way
                file_path = "/home/joel_treichler28/Smart-list/static/profile_pic/indivdual.jpg"

            else:
                file_path = "static/profile_pic/indivdual.jpg"
            with open(file_path, "wb") as file:
                file.write(form_img.content)

            my_user.profile_picture = file_path

            db.session.commit()

            return render_template("my_profile,html",
                                   name=name,
                                   username=username,
                                   email=email,
                                   form=form,
                                   form_img=form_img,
                                   User=User)

        return render_template("my_profile.html",
                               name=name,
                               username=username,
                               email=email,
                               form=form,
                               form_img=form_img,
                               User=User)
    else:
        return redirect(url_for("login"))


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
@login_required
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
    hashed_password = hashed_password.decode("utf-8", "ignore")
    user = User(fname=form_data.fname.data,
                lname=form_data.lname.data,
                uname=form_data.uname.data,
                email=form_data.email.data,
                password=hashed_password)
    db.session.add(user)
    db.session.commit()
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
    current_id = current_user.id
    my_user = User.query.filter_by(id=current_id).first()
    if my_user is None:
        return False
    name = my_user.fname + " " + my_user.lname
    username = my_user.uname
    email = my_user.email
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
    for item in current_df['item']:
        item = item.upper()
    top_n_lst = current_df['item'].value_counts()[:num_of_items].index.tolist()

    img_lst = []
    for i in top_n_lst:
        i = i.replace("!", "_").replace("?", "_").replace("-", "_").replace("/", "_")\
             .replace("%", "_").replace("&", "_").replace(":", "_").replace(";", "_")

        img_url = search_img(i)
        filename = i.split()[0] + ".jpg"
        filepath = save_img(img_url, "static/data/", filename)

        img_lst.append(filepath)

    data = {"item": top_n_lst,
            "path": img_lst}
    top_n_df = pd.DataFrame(data, columns=["item", "path"])
    return top_n_df


def search_img(search_query):
    url = "https://api.unsplash.com/search/photos/"
    parameter = {"client_id": access_key,
                 "query": search_query}
    r = requests.get(url, params=parameter)
    data = r.json()
    try:
        url_raw = data["results"][0]["urls"]["small"]
        return url_raw
    except:
        default_url = "https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483296.jpg"
        return default_url


def save_img(img_url, folder_prefix, filename):
    img = requests.get(img_url)
    if platform == "linux" or platform == "linux2":
        file_path = folder_prefix + filename
    else:
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
        'x-rapidapi-key': APIKEY,
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
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"  \
        + idn + "/information"
    headers = {
        'x-rapidapi-key': APIKEY,
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    response = response.json()
    ingredients = []
    for i in range(0, len(response["extendedIngredients"])):
        string_w_comments = response["extendedIngredients"][i]["originalString"]
        stripped = string_w_comments.split(" (", 1)[0]
        stripped = stripped.split(" -", 1)[0]
        ingredients.append(stripped)
    return ingredients


if __name__ == "__main__":
    if platform == "linux" or platform == "linux2":
        app.run(debug=False, host="10.132.0.5", port=80)
    else:
        app.run(debug=True)

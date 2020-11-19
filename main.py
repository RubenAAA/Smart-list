# import pandas as pd
# import os
import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user
from flask_login import logout_user, login_required
from forms import RegistrationForm, LoginForm, receipt_upload, Upload_product
# for advanced functionalities add following:
# from forms import  receipt_upload, keyword, food_upload
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


@app.route("/")
def index():
    # The smart shopping list
    # Placeholder
    form = Upload_product()


    return render_template("index.html", form=form)


@app.route("/upload-receipt")
def manual_receipt():
    form = receipt_upload()
    if form.validate_on_submit():
        return True  # Placeholder
    return render_template("receipt.html", form=form)


"""
Advanced functionalities

@app.route("/Analytics")
def analytics():
    # The fancy expense report
    return False


@app.route("/scan-receipt")
def receipt():
    # Scan receipt and upload its contents
    form = RegistrationForm()


@app.route("/suggested-recipe")
def sugrec():
    # Recipe from picture
    form = RegistrationForm()


@app.route("/find-recipe")
def findrec():
    #  Recipe from keyword
    form = RegistrationForm()
"""


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()

    if form.validate_on_submit():
        registration_worked = register_user(form)
        if registration_worked:
            return redirect(url_for("login"))

    return render_template("register.html", form=form, User=User)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()

    if form.validate_on_submit():
        if is_login_successful(form):
            return redirect(url_for("index"))
        else:
            if User.query.filter_by(email=form.email.data).count() > 0:
                flash("Login unsuccessful, please check your credentials"
                      "and try again")
            else:
                return redirect(url_for("register"))
    return render_template("login.html", form=form, User=User)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# functions


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


def add_post(form_data):

    posts = Posts(post_content=form_data.text.data,
                  user_id=current_user.id
                  )

    db.session.add(posts)

    db.session.commit()

    return True

if __name__ == "__main__":
    app.run(debug=True)

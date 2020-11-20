from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
# We need the following two for the file upload forms:
# from flask_wtf.file import FileField
# from flask_wtf import Form


class RegistrationForm(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired()])
    lname = StringField("Last Name", validators=[DataRequired()])
    uname = StringField("User Name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit_button = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit_button = SubmitField("Submit")


class receipt_upload(FlaskForm):
    grain = StringField("Grain-based products")
    milk = StringField("Milk-based products")
    proteins = StringField("Proteins")
    vegetables = StringField("Vegetables")
    fruits = PasswordField("Fruits")
    drinks = StringField("Drinks")
    misc = StringField("Miscellaneous")
    submit_button = SubmitField("Submit")


class button_for_script(FlaskForm):
    item = StringField("Product", validators=[DataRequired()])
    submit_button = SubmitField("Submit")

class button1_for_script(FlaskForm):
    submit_button = SubmitField("Save List")

"""
Advanced functionalities

class receipt_upload_adv(Form):
    receipt_picture = FileField("Upload your receipt",
                                            validators=[DataRequired()])
    submit_button = SubmitField("Submit")


class food_upload(Form):
    food_picture = FileField("Upload a picture of your food",
                                        validators=[DataRequired()])
    submit_button = SubmitField("Submit")

class keyword(Form):
    kw_entry = StringField("What do you want to find a recipe for?",
                                        validators=[DataRequired()])
    submit_button = SubmitField("Submit")
"""

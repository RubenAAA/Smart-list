from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, PasswordField, RadioField, TextAreaField, IntegerField
from flask_wtf.file import FileField
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
    greens = StringField("Greens")
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
class Select_recipe(Form):
    recipe_chosen = RadioField(
        'Choose the recipe you want to add to your shopping list', coerce=int)
    submit_button = SubmitField('Submit')
"""


class Trytest(Form):
    number = IntegerField(validators=[DataRequired()])
    submit_button = SubmitField('Submit')


class keyword(Form):
    query = StringField("Enter a keyword for a recipe.",
                        validators=[DataRequired()])
    diet = StringField(
        "Enter a diet if you follow one [vegan, vegetarian, gluten free, dairy free, paleo, etc.]")
    excludeIngredients = TextAreaField(
        "Enter some ingredients that you do not want to be used in the recipe. Separate by a comma and a space if multiple")
    intolerances = TextAreaField(
        "Enter foods you are intolerant to. Separate by a comma and a space if multiple")
    submit_button = SubmitField("Confirm your query and press display recipes button")


class user_preference(FlaskForm):
    preference = StringField("Change the amount of default items displayed")
    submit_button = SubmitField("Submit")


"""
Advanced functionalities

class receipt_upload_adv(Form):
    receipt_picture = FileField("Upload your receipt",
                                            validators=[DataRequired()])
    submit_button = SubmitField("Submit")




class food_upload(Form):
    food_picture = FileField("Upload a picture of your food")
    submit_button = SubmitField("Submit")
"""

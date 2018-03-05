from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Regexp

from re import IGNORECASE


class IndentifyUserForm(FlaskForm):

    email = StringField(
        "email",
        validators=[
            DataRequired("Please enter your nerdery email."),
            Email("Please enter a valid email."),
            Regexp("\w.*@nerdery\.com$", flags=IGNORECASE, message="Please enter your Nerdery email.")
    ])


class VoteSnackForm(FlaskForm):

    @classmethod
    def add_dynamic_fields(cls, list_snacks):
    # set form fields as VoteSnackForm's class attribute
        for i in range(len(list_snacks)):
                setattr(cls, "snack_"+str(i), BooleanField(list_snacks[i]["name"]))


class Test1:
    test_attr = 1
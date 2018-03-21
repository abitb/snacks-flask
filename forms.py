from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Regexp

from re import IGNORECASE


class IndentifyUserForm(FlaskForm):

    email = StringField(
        "email",
        validators=[
            DataRequired("Please enter your nerdery email."),
            Email("Please enter a valid email."),
            Regexp("\w.*@nerdery\.com$", flags=IGNORECASE, message="Please enter your Nerdery email.")]
        )


class VoteSnackForm(FlaskForm):

    _snacks = []

    @classmethod
    def add_dynamic_fields(cls, list_snacks):
        """
        This static method allows adding dynamic fields to VoteSnackForm
        :param list_snacks: [{"snack name": "12/06/2017"},...]
        """
        # delete previously exisiting class attributes
        if cls._snacks:
            for s in cls._snacks:
                delattr(cls, s)
            cls._snacks[:] = []

        # set form fields as VoteSnackForm's class attribute
        # example: cls.snack_0 = BooleanFields("pennuts")
        for i in range(len(list_snacks)):
            cls._snacks.append("snack_"+str(i))
            setattr(cls, "snack_"+str(i), BooleanField(list_snacks[i]["name"]))


class SuggestionDropdown(FlaskForm):

    snack_options = SelectField("Select a snack from the list")
    suggestion_input = StringField("suggestion")
    suggestion_location = StringField("location")

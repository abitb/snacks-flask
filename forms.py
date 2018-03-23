from re import IGNORECASE

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Regexp
from wtforms.validators import ValidationError


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
        :param list_snacks: [snack name,...]
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
            setattr(cls, "snack_"+str(i), BooleanField(list_snacks[i]))


def no_white_space(form, field):
    """
    Custom validator, a callable raises ValidationError
    Make sure a user input contains only white spaces is not accepted
    """
    if len(field.data) > 0 and (not field.data.strip()):
        raise ValidationError("Invalid input.")


class SuggestionDropdown(FlaskForm):

    snack_options = SelectField("Select a snack from the list", choices=[("","Please select")])
    suggestion_input = StringField("suggestion", validators=[no_white_space])
    suggestion_location = StringField("location", validators=[no_white_space])

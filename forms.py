from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
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

	submit = SubmitField("Submit")

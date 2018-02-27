from flask_wft import form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class IndentifyUserForm(Form):
	email = StringField("email",validators=[
		DataRequired("Please enter your nerdery email."),
		Email("Please enter your nerdery email."),
		Regexp("@nerdery\.com$", message="Please enter your nerdery email.")
		])
	submit = SubmitField("Submit")

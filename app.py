from datetime import date

from flask import Flask, render_template, request, session, redirect, url_for, flash

from config import config
import webservice_client
import model
from forms import *


# Default port is 5000.
app = Flask(__name__)
# Take configuration from config.py.
app.config.from_object(config["development"])
# Set sqlite database location
model.Models.DB_FILE = app.config["DATABASE_URI"]
webservice_client.APIKEY = app.config["API_KEY"]


@app.route("/", methods=["GET","POST"])
def index():
    # Make sure any user who can see the pages have provided their nerdery email.
    if "email" not in session:
        return redirect(url_for("register"))

    print session["email"]

    # Initialize container for keyword args to be passed to the view
    snacks = {}
    # Initialize model for this user
    model_vote = model.Votes(session["email"])
    # The allowed vote count left for user is need for both GET and POST
    allowed_vote = model_vote.get_allowed_votes()

    # When user request to view the page, get data to display.
    if request.method == "GET":
        resp = webservice_client.get_snacks_from_web_service()

    # When web service is down, redirect.
        if not resp:
            return redirect(url_for("no_ws"))

        today = date.today()

        always_purchased, optional_snacks = webservice_client.separate_optional_snacks(resp)
        suggested_snacks = model_vote.get_suggestion(year=today.year, month=today.month)

        if len(suggested_snacks) == 0:
            snacks["error_no_suggestion"] = "Please suggest some snacks!"

    # Use optional snacks from webservice to create vote form
        snacks_pruchase_date = {s["name"]: s["lastPurchaseDate"] for s in optional_snacks}
    # Dynamically add fields (VoteSnackForm's class attribute) corresponding to each snack
        VoteSnackForm.add_dynamic_fields(suggested_snacks)
        form = VoteSnackForm()

    # Get this month's suggestion vote
        ranked_snacks = model_vote.get_tally(year=today.year, month=today.month)

        snacks.update({
            "allowed_vote": allowed_vote,
            "always_purchased": always_purchased,
            "ranked_snacks": ranked_snacks,
            "snacks_pruchase_date": snacks_pruchase_date,
            "form": form
                })
    # GET will render view
        return render_template("pages/index.html", **snacks)

    # When user submitted vote, process the interaction.
    if request.method == "POST":

        form = VoteSnackForm()

        if form.validate():
    # Get votes from user input
            votes = []
            for field in form:
                if "snack" in field.name and field.data == True:
                    votes.append(field.label.text)

    # Success: pass all validations and record the votes
            if len(votes) <= allowed_vote:
                model_vote.register_votes(votes)
    # Error1:
            else:
                flash("You exceed the maximum allowed votes for this month.", "error_vote")
    # Error2: Form input is not valid, not doing anything to database
        else:
            print form.errors

    # POST will always redirect
        return redirect(url_for("index"))


@app.route("/suggestions", methods=["GET","POST"])
def suggestions():
    # Make sure any user who can see the pages have provided their nerdery email.
    if "email" not in session:
        return redirect(url_for("register"))

    # Initialize container for keyword args to be passed to the view
    snacks = {}
    # Initialize model for this user
    model_vote = model.Votes(session["email"])
    today = date.today()

    # Prepare not yet voted on suggestions using web service
    resp = webservice_client.get_snacks_from_web_service()
    # When web service is down, redirect.
    if not resp:
        return redirect(url_for("no_ws"))

    # Get optional snacks from web service, subtract the already suggested snacks
    optional_snacks = webservice_client.separate_optional_snacks(resp)[1]

    l_optional_snacks = [s["name"] for s in optional_snacks]
    suggested_snacks = model_vote.get_suggestion(year=today.year, month=today.month)
    optional_not_suggested = list(set(l_optional_snacks)-set(suggested_snacks))

    # Construct form for the view
    form_suggestion = SuggestionDropdown()
    choices = [("","Please select")]+[(s, s) for s in optional_not_suggested]
    form_suggestion.snack_options.choices = choices

    # When user request to view the suggestion page
    if request.method == "GET":

    # If already voted this month, set error message
        if today.strftime("%Y-%m") == model_vote.get_last_suggest_date():
            snacks["error_suggestion"] = "There is a total of one allowed suggestion per month."

        snacks.update({
            "form": form_suggestion
            })
    # GET will render view
        return render_template("pages/suggestions.html", **snacks)

    if request.method == "POST":

        dropdown_input = form_suggestion.snack_options.data
        text_suggestion = form_suggestion.suggestion_input.data
        text_location = form_suggestion.suggestion_location.data

    # Error0 : already suggested, don't process form
        if today.strftime("%Y-%m") == model_vote.get_last_suggest_date():
            flash("You have attempted to add more than the allowed number of suggestions per month!", "error_suggestion")
            return redirect(url_for("suggestions"))

        if form_suggestion.validate():
            dropdown_input = form_suggestion.snack_options.data
            text_suggestion = form_suggestion.suggestion_input.data
            text_location = form_suggestion.suggestion_location.data

    # Error1: more than one suggestion
            if dropdown_input and text_suggestion:
                flash("Please choose one between selecting from drop-down or entering a new suggestion.", "error_suggestion")
    # Success1: user submits one drop-down item, record suggestion by updating db
            if dropdown_input and (not text_suggestion):
                model_vote.suggest(dropdown_input)
                return redirect(url_for("index"))
    # User manually inputs a new suggestion
            if (not dropdown_input) and text_suggestion:
    # With location, Post to web service
                if text_location:
                    post_resp = webservice_client.post_snack_to_web_service(name=text_suggestion, location=text_location)
    # Success2: If success, record suggestion for this month too
                    if post_resp == 200:
                        model_vote.suggest(text_suggestion)
                        return redirect(url_for("index"))
    # Error2: duplicate
                    elif post_resp == 409:
                        flash("You have attempted to add a suggestion that already exists!", "error_duplicate")
    # Error3: not enough info
                else:
                    flash("You have not completed information requested.", "error_completion")

            if (not dropdown_input) and (not text_suggestion):
                flash("You have not completed information requested.", "error_completion")
        else:
            print form_suggestion.errors

    # POST will always redirect
        return redirect(url_for("suggestions"))


@app.route("/register", methods=["GET","POST"])
def register():
    if "email" in session:
        return redirect(url_for("index"))

    # Create form object to display, and use
    form = IndentifyUserForm()

    # When user summited email
    if form.validate_on_submit():
    # If input is validate, set session, and redirect to vote page
        user_email = form.email.data.lower()
        session["email"] = user_email
        return redirect(url_for("index"))

    return render_template("pages/register.html", form=form)


@app.route("/servicedown")
def no_ws():
    return render_template("pages/servicedown.html")


@app.route("/logout")
def log_out():
    session.clear()
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('pages/500.html'), 500



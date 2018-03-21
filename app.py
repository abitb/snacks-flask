from datetime import date

from flask import Flask, render_template, request, session, redirect, url_for, flash

from config import config
import webservice_client
import model
from forms import *


# Default port is 5000.
app = Flask(__name__)
# Take configuration from config.py.
app.config.from_object(config['development'])
# Set sqlite database location
model.Models.db_file = config['development'].DATABASE_URI
webservice_client.ApiKey = config['development'].API_KEY


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
    snacks["allowed_vote"] = model_vote.get_allowed_votes()

    # When user request to view the page, get data to display.
    if request.method == "GET":
        resp = "resp"
        # resp = webservice_client.get_snacks_from_web_service()
        if resp:
        #     always_purchased, optional_snacks = webservice_client.separate_optional_snacks(resp)

            optional_snacks = []
            if len(optional_snacks) == 0:
                snacks["error_no_suggestion"] = "Please suggest some snacks!"

            # Initialize information to be displayed in template
            # optional_snacks = [
            #     {"id": 2000, "lastPurchaseDate": "12/1/2014", "name": "Donuts", "optional": True, "purchaseCount": 1, "purchaseLocations": ""},
            #     {"id": 2001, "lastPurchaseDate": "12/1/2014", "name": "Spam", "optional": True, "purchaseCount": 1, "purchaseLocations": ""},
            #     {"id": 2002, "lastPurchaseDate": "12/1/2014", "name": "Buckets of M&M's", "optional": True, "purchaseCount": 1, "purchaseLocations": ""},
            #     {"id": 2002, "lastPurchaseDate": "10/1/2014", "name": "Pistachios", "optional": True, "purchaseCount": 1, "purchaseLocations": ""},
            # ]
    # Use optional snacks from webservice to create vote form
            snacks["optional_snacks_date"] = {s["name"]: s["lastPurchaseDate"] for s in optional_snacks}
    # Dynamically add fields (VoteSnackForm's class attribute) corresponding to each snack
            VoteSnackForm.add_dynamic_fields(optional_snacks)
            form = VoteSnackForm()

    # Get this month's suggestion vote
            today = date.today()
            snacks["ranked_snacks"] = model_vote.get_tally(year=today.year, month=today.month)

            print "get "

            always_purchased = [
                {"id": 2005, "lastPurchaseDate": "12/1/2014", "name": "Pop Tarts", "optional": False, "purchaseCount": 1, "purchaseLocations": ""},
                {"id": 2006, "lastPurchaseDate": "12/1/2014", "name": "Bagels", "optional": False, "purchaseCount": 1, "purchaseLocations": ""},
                {"id": 2007, "lastPurchaseDate": "12/1/2014", "name": "Ramen Noodles", "optional": False, "purchaseCount": 1, "purchaseLocations": ""},
                {"id": 2008, "lastPurchaseDate": "10/1/2014", "name": "Cereal", "optional": False, "purchaseCount": 1, "purchaseLocations": ""},
                {"id": 2009, "lastPurchaseDate": "10/1/2014", "name": "Trail Mix", "optional": False, "purchaseCount": 1, "purchaseLocations": ""},
            ]
    # Set always purchased snacks to be passed to view
            snacks["always_purchased"] = always_purchased


    # When web service is down, set error.
        else:
            snacks["error_ws"] = "Sorry, we can't get snack information from OCD right now."

    # When user submitted vote, process the interaction.
    if request.method == "POST":
    #     for field in form:
    #         print field
        print "POST "

        form = VoteSnackForm()
        if form.validate():
            votes = []
            for field in form:
                if "snack" in field.name and field.data == True:
                    votes.append(field.label.text)

            print votes
            if len(votes) <= snacks["allowed_vote"]:
                model_vote.register_votes(votes)
            else:
                flash("You exceed the maximum allowed votes for this month.", "error_vote")
                print "else"
        else:
            print form.errors

    # POST will always redirect
        return redirect(url_for("index"))

    # If post:
    #   Get vote from request
    #   If vote.count > user. Get_allowed_vote()
    #       set error_message
    #   Else
    #       Validate vote number
    #       Vote.Register_votes(vote)
    # Display with error
    #
    return render_template("pages/index.html", form=form, **snacks)


@app.route("/suggestions", methods=["GET","POST"])
def suggestions():
    # Make sure any user who can see the pages have provided their nerdery email.
    if "email" not in session:
        return redirect(url_for("register"))

    snacks = {}
    model_vote = model.Votes(session["email"])

    # Get suggesion list from api
    if request.method == "GET":

        resp = webservice_client.get_snacks_from_web_service()
        if resp:
            always_purchased, optional_snacks = webservice_client.separate_optional_snacks(resp)
    # Prepare suggestion form for the view
            form_suggestion = SuggestionDropdown()
            form_suggestion.snack_options.choices = [("snack_" + str(i), s["name"]) for i, s in enumerate(optional_snacks)]
            snacks["form_suggestion"] = form_suggestion

    # If already voted this month, set error message
            if date.today().strftime("%Y-%m") == model_vote.get_last_suggest_date():
                snacks["error_suggestion"] = (
                    "You have attempted to add more than the allowed number of suggestions per month!",
                    "There is a total of one allowed suggestion per month.")

    # If no web service, set error message
        else:
            snacks["error_ws"] = "Sorry, we can't get snack information from OCD right now."

    # Else:
    #     If post:
    #         Validate input
    #         (more than one, only one from list, no data?)
    #         If not valid:
    #             Set error
    #         Else:
    #             Make request to remote api
    #             Get response
    #             If resp.status_code= 200:
    #                 Put timestamp in session
    #             If resp.status_code = 409:
    #                 Set error

    # Display with error, message

    return render_template("pages/suggestions.html", **snacks)

@app.route("/register", methods=["GET","POST"])
def register():
    if "email" in session:
        return redirect(url_for("index"))

    # Create form object to display, and use
    form = IndentifyUserForm()

    # When user summited email
    if request.method == "POST":
        # If input is validate, set session, and redirect to vote page
        if form.validate():
            user_email = form.email.data.lower()
            session["email"] = user_email
            return redirect(url_for("index"))

    return render_template("pages/register.html", form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



from flask import Flask, render_template, request, session, redirect, url_for

from config import config
import webservice_client
import model
from forms import *

from datetime import date


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

    # Initialize information to be displayed in template
    snacks = {}

    print session["email"]
    model_vote = model.Votes(session["email"])
    allowed_vote = model_vote.get_allowed_votes()

    # When user request to view the page, get data to display.
    if request.method == "GET":
        # resp = webservice_client.get_snacks_from_web_service()

        Test1.test_attr += 1
        c = Test1()
        print "get ",
        print Test1.test_attr

        # if resp:
        #     always_purchased, optional_snacks = webservice_client.separate_optional_snacks(resp)

    today = date.today()
    snacks["snack_tally"] = model_vote.get_tally(today.month, today.year)
    snacks["snack_tally"] = {"Donuts":3, "Spam":2}
    snacks["ranked_snacks"] = snacks["snack_tally"].keys()

    optional_snacks = [
        {"id": 2000, "lastPurchaseDate": "12/1/2014", "name": "Donuts", "optional": True, "purchaseCount": 1, "purchaseLocations": ""},
        {"id": 2001, "lastPurchaseDate": "12/1/2014", "name": "Spam", "optional": True, "purchaseCount": 1, "purchaseLocations": ""},
        {"id": 2002, "lastPurchaseDate": "12/1/2014", "name": "Buckets of M&M's", "optional": True, "purchaseCount": 1, "purchaseLocations": ""},
        {"id": 2002, "lastPurchaseDate": "10/1/2014", "name": "Pistachios", "optional": True, "purchaseCount": 1, "purchaseLocations": ""},
    ]

    # Dynamically add fields (class attribute of custom form) using optional snacks from webservice
    # Form fields correspond to snacks in optional_snacks
    # todo: has dynamic flag
    VoteSnackForm.add_dynamic_fields(optional_snacks)
    # Have super constructor register fields
    form = VoteSnackForm()

    snacks["optional_snacks"] = {s["name"]: s["lastPurchaseDate"] for s in optional_snacks}

    # If web service is down, set error.
        # else:
        #     snacks["error":"Sorry, we can't get snack information from OCD right now." ]
        #     always_purchased, optional_snacks = ([],[])

    # When user submitted vote, process the interaction.
    if request.method == "POST":
    #     for field in form:
    #         print field
        c = Test1()
        print "POST, "
        print Test1.test_attr
        form = VoteSnackForm()

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


@app.route("/suggestions")
def suggestions():
    return render_template("pages/suggestions.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if "email" in session:
        return redirect(url_for("index"))

    # Create form object to display, and use
    form = IndentifyUserForm()

    # When user submmited email
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



from flask import Flask, render_template, request, session, redirect, url_for

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

    error = {}
    snacks = {}

    model_vote = model.Votes(session["email"])
    allowed_vote = model_vote.get_allowed_votes()

    # When user request to view the page, get data to display.
    if request.method == "GET":
        resp = webservice_client.get_snacks_from_web_service()

        if resp:
            always_purchased, suggested_so_far = webservice_client.separate_optional_snacks(resp)
            snack_tally = model_vote.get_tally()

            suggested_so_far = [
                {"id": 2000, "lastPurchaseDate": "12/1/2014", "name": "Donuts", "optional": True, "purchaseCount": 1, "purchaseLocations": ""},
                {"id": 2001, "lastPurchaseDate": "12/1/2014", "name": "Spam", "optional": True, "purchaseCount": 1, "purchaseLocations": ""},
                {"id": 2002, "lastPurchaseDate": "12/1/2014", "name": "Buckets of M&M's", "optional": True, "purchaseCount": 1, "purchaseLocations": ""},
                {"id": 2002, "lastPurchaseDate": "10/1/2014", "name": "Pistachios", "optional": True, "purchaseCount": 1, "purchaseLocations": ""},
            ]
    # If web service is down, set error.
        else:
            error["error":"Sorry, we can't get snack information from OCD right now." ]
            always_purchased, suggested_so_far = ([],[])

    # When user submitted vote, process the interaction.
    if request.method == "POST":
        pass

    # If post:
    #   Get vote from request
    #   If vote.count > user. Get_allowed_vote()
    #       set error_message
    #   Else
    #       Validate vote number
    #       Vote.Register_votes(vote)
    # Display with error
    #
    return render_template("pages/index.html")


@app.route("/suggestions")
def suggestions():
    return render_template("pages/suggestions.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if "email" in session:
        return redirect(url_for("index"))

    # Create form object to display, and use
    form = IndentifyUserForm(request.form)

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



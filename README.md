To set up development database, go to project directory:
python model.py

About database:
tb_votes:
- vote_date: useful for getting a tally of votes and remaining votes for each email on a particular month
- user_email: used to identify each user, and to set session

tb_suggestion: used to make sure one suggestion per email per month

To test run development server:
set FLASK_APP=app.py
set FLASK_DEBUG=1
flask run

Then go to:
http://127.0.0.1:5000/


1) I will use a library instead of writing my own database access script
2) I would open and close databse connection per request instead of per each record access
3) have proper unit testing
4) better exception handling
5) pay more attention to site security
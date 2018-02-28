set FLASK_APP=app.py
set FLASK_DEBUG=1
flask run


database:
tb_votes:
- vote_date: would be compare to the current month to get a tally of votes and remaining votes for each user email
- user_email
- voted_snack

1) I will use a library instead of writing my own database access script
2) I would open and close databse connection per request instead of per each record access
3) have proper unit testing
4) better exception handling
5) pay more attention to site security
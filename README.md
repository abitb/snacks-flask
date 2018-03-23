## Nedery NAT in Python Flask

### Database:
tb_votes:
- vote_date: useful for getting a tally of votes and remaining votes for each email for a particular month
- user_email: value taken from session, used to identify each user

tb_suggestion:
- used to make sure one suggestion per email per month, and to get a list of suggestions to be voted on this month

### Directory:
| File | description |
| ------ | ------ |
| config.py | Stores configuration, contains only development configuration right now |
| DBConnection.py | A minimalistic library allowing the usage of sqlite database in model |
| model.py | Model |
| /templates/ | View |
| app.py | Routes and main logic (controller) |
| webservice_client.py | Contains functions to make requests to Nerdery Snack Food API |
| /static/assets/ | Styles |

### To test run development server
go to project directory

First install required packages:
```sh
pip install -r requirements.txt
```
Then set up development database:
```sh
python model.py
```
Set up development variables in terminal (I use windows):
```sh
set FLASK_APP=app.py
```
Optional: set FLASK_DEBUG=1
```sh
flask run
```
Then go to:
http://127.0.0.1:5000/

### This is a prototype on development server
Flask's development server only accommodates one user connection at a time.
To be able to serve multiple users, this project needs to be deployed to a WSGI server and let server handles the load.

### To make this project suitable for deployment:
1) I would use a library instead of writing my own database access script
2) I would open and close database connection per request instead of per each record access
3) have proper unit testing
4) better exception handling
5) pay more attention to site security
6) finish up the deployment part

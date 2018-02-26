from flask import Flask, render_template, request, session, redirect, url_for
import routes

# default port 5000
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('pages/index.html')
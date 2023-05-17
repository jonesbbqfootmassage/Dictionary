from flask import Flask, render_template, redirect, request, session
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt

app = Flask(__name__)


@app.route('/')     # calls main page
def render_homepage():
    return render_template('home.html')


@app.route('/vocab')     # calls vocabulary page
def render_vocab():

    return render_template('vocab.html')


app.run(host='0.0.0.0', debug=True)
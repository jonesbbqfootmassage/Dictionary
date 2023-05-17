from flask import Flask, render_template, redirect, request, session
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt

app = Flask(__name__)
DATABASE = "C:/Users/lante/OneDrive - Wellington College/2023/13DTS/Maori/maori_words.db"


def open_database(db_file):     # function to connect to database
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


@app.route('/')     # calls main page
def render_homepage():
    return render_template('home.html')


@app.route('/vocab')     # calls vocabulary page
def render_vocab():
    con = open_database(DATABASE)
    query = "SELECT * FROM words_list WHERE cat_id = ? ORDER BY Category"
    return render_template('vocab.html')


app.run(host='0.0.0.0', debug=True)
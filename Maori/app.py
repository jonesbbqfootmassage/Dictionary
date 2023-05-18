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


def is_logged_in():     # shows if or if not logged in
    if session.get("email") is None:
        print("not Logged in")
        return False
    else:
        print("Logged in")
        return True


@app.route('/')     # calls main page
def render_homepage():
    return render_template('home.html')


@app.route('/vocab/<cat_id>')     # calls vocabulary page
def render_vocab(cat_id):
    con = open_database(DATABASE)
    query = "SELECT * FROM category_table"
    cur = con.cursor()
    cur.execute(query)
    category_list = cur.fetchall()
    print(category_list)

    query = "SELECT * FROM words_list WHERE cat_id= ? ORDER BY ID"
    cur = con.cursor()
    cur.execute(query, (cat_id, ))
    words_list = cur.fetchall()
    print(words_list)
    con.close()

    return render_template('vocab.html', words=words_list, categories=category_list     )




app.run(host='0.0.0.0', debug=True)
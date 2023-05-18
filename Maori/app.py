from flask import Flask, render_template, redirect, request, session
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt


DATABASE = "C:/Users/lante/OneDrive - Wellington College/2023/13DTS/Maori/maori_words.db"

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "j0e9jvfdo"    # hashes the password


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
    con = open_database(DATABASE)
    query = "SELECT * FROM words_list"
    cur = con.cursor()
    cur.execute(query)
    words_list = cur.fetchall()
    print(words_list)
    return render_template('home.html', logged_in=is_logged_in())


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

    return render_template('vocab.html', words=words_list, categories=category_list, logged_in=is_logged_in())


@app.route('/login', methods=['POST', 'GET'])
def render_login():
    if is_logged_in():
        return redirect('/?message=Logged+in')
    print("logging in")
    if request.method == "POST":
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip().lower()

        query = """SELECT id, fname, password FROM user WHERE email = ?"""
        con = open_database(DATABASE)
        cur = con.cursor()
        cur.execute(query, (email,))
        user_data = cur.fetchall()
        con.close()
        print(user_data)

        if user_data is None:
            return redirect("/login?error=Email+invalid+or+password+incorrect")

        user_id = user_data[0][0]
        first_name = user_data[0][1]
        db_password = user_data[0][2]

        if not bcrypt.check_password_hash(db_password, password):
            return redirect(request.referrer + "?error=Email+invalid+or+password+incorrect")

        session['email'] = email
        session['user_id'] = user_id
        session['first_name'] = first_name
        print(session)
        return redirect('/')

    return render_template('login.html', logged_in=is_logged_in())


@app.route('/logout')
def logout():
    print(list(session.keys()))
    [session.pop(key) for key in list(session.keys())]
    print(list(session.keys()))
    return redirect('/?message=Bye+bye!')


@app.route('/signup', methods=['POST', 'GET'])
def render_signup():
    if is_logged_in():
        return redirect('/?message=Already+logged+in')
    if request.method == 'POST':
        print(request.form)
        fname = request.form.get('fname').title().strip()
        lname = request.form.get('lname').title()
        email = request.form.get('email').lower().strip()
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            return redirect("\signup?error=Passwords+do+not+match")

        if len(password) < 8:
            return redirect("\signup?error=Password+must+be+at+least+8+characters")

        hashed_password = bcrypt.generate_password_hash(password)
        con = open_database(DATABASE)
        query = "INSERT INTO user (fname, lname, email, password) VALUES (?, ?, ?, ?)"
        cur = con.cursor()

        try:
            cur.execute(query, (fname, lname, email, hashed_password))
        except sqlite3.IntegrityError:
            con.close()
            return redirect("\signup?error=Email+is+already+used")
        con.commit()
        con.close()
        return redirect("/login")

    return render_template('signup.html', logged_in=is_logged_in())



app.run(host='0.0.0.0', debug=True)
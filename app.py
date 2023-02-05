from pymysql import cursors
from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import pymysql
# from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import os
from FinDB import FinDB
from UserLogin import UserLogin

app = Flask(__name__)
# secret key for session
app.config['SECRET_KEY'] = 'hg534khk5hiu5kjn6k3q46b'
# config lifetime of session False = close browser / True =  app.permanent_session_lifetime (default 31 days)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["REMEMBER_COOKIE_DURATION"] = datetime.timedelta(seconds=60)
# Session(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You must be logged in to access'


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    con = get_db()
    dbase = FinDB(con)
    # user_id = session["user_id"]
    return UserLogin().from_db(user_id, dbase)


@app.route("/")
def index():

    return render_template('index.html')


@app.route('/main')
@login_required
def main():
    curr_year = int(datetime.date.today().strftime("%Y"))
    curr_month = int(datetime.date.today().strftime("%m"))
    first_day_month = datetime.date(curr_year, curr_month, 1).strftime('%A')
    cur_user = current_user.__dict__
    month = datetime.date.today().strftime('%B')
    year = datetime.date.today().strftime('%Y')
    day = int(datetime.date.today().strftime('%d'))
    all_months = {'January': 31, 'February': 28, 'March': 31, 'April': 30, 'May': 31, 'June': 30, 'July': 31,
                  'August': 31, 'September': 30, 'October': 31, 'November': 30, 'December': 31}
    if month in ['January', 'March', 'May', 'July', 'August', 'October', 'December']:
        days = [i for i in range(1, 32)]
    elif month == 'February':
        days = [i for i in range(1, 29)]
    else:
        days = [i for i in range(1, 31)]

    return render_template('main.html', cur_user=cur_user, month=month, year=year, day=day, days=days, first_day_month=first_day_month)


@app.route("/login", methods=["GET", "POST"])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main'))
    if request.method == "GET":
        return render_template('login.html')
    else:
        if not request.form.get("username"):
            flash('form must be fill')
            return render_template('/login.html')
        elif not request.form.get("password"):
            flash('form must be fill')
            return render_template('/login.html')
        else:

            con = get_db()
            with con.cursor() as cursor:
                cursor.execute(
                    f"""SELECT * FROM users WHERE username = '{request.form.get("username")}';"""
                )
                user = cursor.fetchall()
                if len(user) != 1 or not check_password_hash(user[0]['hash'], request.form.get("password")):
                    flash("invalid username and/or password")
                    return render_template('/login.html')
                else:
                    flash("ok")
                    rm = True if request.form.get('remain me') else False
                    userlogin = UserLogin().create(user)
                    login_user(userlogin, remember=rm)

                    user_id = user[0]['id']
                    session["user_id"] = user_id
                    return redirect('/main')


@app.route("/logout")
def logout():
    """Log user out"""
    logout_user()
    # Forget any user_id
    session.clear()
    flash('log out')
    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            flash('form must be fill')
            return render_template('/register.html')
        elif not request.form.get("password"):
            flash('form must be fill')
            return render_template('/register.html')
        else:
            if request.form.get('password') == request.form.get('password2'):
                con = get_db()
                with con.cursor() as cursor:
                    cursor.execute(
                        f"""SELECT * FROM users WHERE username = '{request.form.get("username")}';"""
                    )
                    user = cursor.fetchall()
                    print(user)
                    if len(user) != 0:
                        # create flash message 'username already exist'
                        flash('username already exist')
                        return render_template('register.html')
                    else:
                        username = request.form.get('username')
                        password = request.form.get('password')
                        hash_p = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                        try:
                            cursor.execute(
                                f"""INSERT INTO users (username, hash) VALUES ('{username}', '{hash_p}');"""
                            )
                            con.commit()
                            return redirect('/')
                        except Exception as ex:
                            print(ex)
            else:
                flash('passwords not equal')
                return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/restore_psw')
def restore_psw():
    return redirect('/')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('plug.html')


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


def connect_db():
    con = pymysql.connect(
            host='185.114.245.124',
            port=3306,
            user='ca56059_finance',
            password='5EdYsVq6',
            database='ca56059_finance',
            cursorclass=cursors.DictCursor
        )
    print('connect')

    return con


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


if __name__ == "__main__":
    app.run(debug=True)


# @app.after_request
# def after_request(response):
#     """Ensure responses aren't cached"""
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response

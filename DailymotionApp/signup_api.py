from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from signup_dbstatement import insert_user
from signup_config import read_config
from signup_email import send_email
import random
import logging
import datetime


api = Flask(__name__)

API_KEY = "b6907d289e10d714a6e88b30761fae22"
api.config['SESSION_TYPE'] = 'memcached'
api.config['SECRET_KEY'] = API_KEY
app_config = read_config('app_config')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

@api.route('/signup')
def signup():
    return render_template('signup.html')


@api.route('/signup', methods=['POST'])
def signup_post():
    global email
    global password
    email = request.form.get('email')
    password = request.form.get('password')

    global passcode
    passcode = random.randint(1111, 9999)

    send_email(app_config, email, passcode)

    global await_time
    auth_wait = int(app_config["timeout"])
    now_time = datetime.datetime.now()
    await_time = now_time + datetime.timedelta(seconds=auth_wait/1000)

    return redirect(url_for('authenticate_user'))


@api.route('/authenticate')
def authenticate_user():
    return render_template('authenticate.html', timeout=authenticate_time())


@api.route('/authenticate', methods=['POST'])
def authenticate_user_post():
    user_passcode = request.form.get('passcode')
    print(passcode)
    print(user_passcode)
    print(authenticate_time())

    if user_passcode.strip() == str(passcode).strip() and authenticate_time() > 0:
        try:
            insert_user(email, generate_password_hash(password, method='sha256'))

        except Exception as error:
            flash('Issue signing up user. Email address may already exists')
            logging.exception("exception")
            return redirect(url_for('signup'))

    else:
        flash('Incorrect Passcode')
        return render_template('authenticate.html', timeout=authenticate_time())

    return render_template('thankyou.html')


def authenticate_time():
    auth_wait = (await_time - datetime.datetime.now()).total_seconds()
    if auth_wait < 1:
        return 0
    return auth_wait * 1000


if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5000)


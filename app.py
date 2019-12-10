from flask import Flask, render_template, request, Response, make_response, redirect, url_for
import psycopg2
import hashlib
import redis

from classes.db_connection import DB_connection
from classes.requests import *

app = Flask(__name__)
redis_instance = redis.Redis(db=4)

@app.route('/')
def auth():
    if 'flask_adminka_authorized_user_id' in request.cookies:
        return redirect('/admin')

    return render_template('auth.html')


@app.route('/registration')
def registration():
    if 'flask_adminka_authorized_user_id' in request.cookies:
        return redirect('/admin')

    return render_template('registration.html')


@app.route('/admin')
def admin():    
    if 'flask_adminka_authorized_user_id' not in request.cookies:
        return redirect('/', code=404)

    id_auth_user = request.cookies.get('flask_adminka_authorized_user_id')


    cache = get_admin_tpl_redis(id_auth_user)
    if cache:
        return cache
    else:
        return get_admin_tpl_postgres(id_auth_user)


@app.route('/auth_request', methods=['POST'])
def auth_request():
    with DB_connection() as db_connect:
        db_cursor = db_connect.cursor()

        pasword = request.values.get('password')
        password_hash = hashlib.sha1(pasword.encode('ASCII')).hexdigest()
        email = request.values.get('email')

        try:
            req = "select * from users where password_hash='" + password_hash + "' and email='" + email + "' and active=TRUE"
            db_cursor.execute(req)
            user = str(db_cursor.fetchone()[0])

            db_connect.commit()

            resp = Response('authorized')
            resp.headers['Set-Cookie'] = 'flask_adminka_authorized_user_id=' + user
            return resp            
        except:
            return Response('not authorized')


@app.route('/registration_request', methods=['POST'])
def registration_request():
    pasword = request.values.get('password')
    password_hash = hashlib.sha1(pasword.encode('ASCII')).hexdigest()
    email = request.values.get('email')        

    return registration_tpl(password_hash, email)


@app.route('/submit_profile_request', methods=['POST'])
def submit_profile_request():
    firstname = request.values.get('firstname')
    lastname = request.values.get('lastname')
    id_auth_user = request.cookies.get('flask_adminka_authorized_user_id')

    with DB_connection() as db_connect:
        db_cursor = db_connect.cursor()
        req = "select * from options where user_id=" + id_auth_user
        db_cursor.execute(req)
        record = db_cursor.fetchone() 

        if record:
            return set_postgres_names(firstname, lastname, id_auth_user, db_cursor, db_connect)
        else:
            return Response('failed')


@app.route('/submit_notepad_request', methods=['POST'])
def submit_notepad_request():
    notepad = request.values.get('notepad')
    id_auth_user = request.cookies.get('flask_adminka_authorized_user_id')

    with DB_connection() as db_connect:
        db_cursor = db_connect.cursor()

        req = "select * from options where user_id=" + id_auth_user
        db_cursor.execute(req)
        record = db_cursor.fetchone() 

        if record:
            return set_postgres_notepad(notepad, id_auth_user, db_cursor, db_connect)
        else:
            return Response('failed')



@app.route('/logout_request', methods=['POST'])
def logout_request():
    return logout()

if __name__ == '__main__':
    app.run()
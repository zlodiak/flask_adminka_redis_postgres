import redis
import psycopg2
from flask import Response, render_template, request

from classes.db_connection import DB_connection
from classes.exceptions import *


redis_instance = redis.Redis(db=4)


def set_redis_notepad(notepad, id_auth_user):
    try:
        with redis_instance.pipeline() as pipe:
            pipe.multi()
            pipe.set('notepad:' + id_auth_user, notepad)
            pipe.execute()
            redis_instance.bgsave()
    except psycopg2.OperationalError as e:
        raise RedisSetOperationException    


def set_redis_names(firstname, lastname, id_auth_user):
    try:
        with redis_instance.pipeline() as pipe:
            pipe.multi()
            pipe.set('firstname:' + id_auth_user, firstname)
            pipe.set('lastname:' + id_auth_user, lastname)
            pipe.execute()
            redis_instance.bgsave()
    except psycopg2.OperationalError as e:
        raise RedisSetOperationException  


def set_postgres_names(firstname, lastname, id_auth_user, db_cursor, db_connect):
    try: 
        req = "UPDATE options SET firstname='" + firstname + "', lastname='" + lastname + "' WHERE user_id=" + str(id_auth_user)
        db_cursor.execute(req);

        set_redis_names(firstname, lastname, id_auth_user)

        db_connect.commit()

        return Response('submit profile is complete')
    except (RedisSetOperationException, psycopg2.OperationalError) as e:
        return Response('failed', e)


def set_postgres_notepad(notepad, id_auth_user, db_cursor, db_connect):
    try: 
        req = "UPDATE options SET notepad='" + notepad + "' WHERE user_id=" + str(id_auth_user)
        db_cursor.execute(req)

        set_redis_notepad(notepad, id_auth_user)

        db_connect.commit()

        return Response('submit notepad is complete')
    except (RedisSetOperationException, psycopg2.OperationalError) as e:
        return Response('failed', e)


def get_admin_tpl_postgres(id_auth_user):
    with DB_connection() as db_connect:
        admin_forms_values = {
            'firstname': None,
            'lastname': None,
            'notepad': None,
        }

        db_cursor = db_connect.cursor()

        try:
            request_form = "select * from options where user_id='" + id_auth_user + "'"
            db_cursor.execute(request_form)
            record = db_cursor.fetchone()
            admin_forms_values['firstname'] = record[1] if record[1] else ''
            admin_forms_values['lastname'] = record[2] if record[2] else ''
            admin_forms_values['notepad'] = record[3] if record[3] else ''
            print('log: successfull retrieve admin_forms_values', admin_forms_values)
        except:
            print('log: failed retrieve admin_forms_values', admin_forms_values)
        
        return render_template('admin.html', admin_forms_values=admin_forms_values)


def get_admin_tpl_redis(id_auth_user):
    admin_forms_values = {
        'firstname': None,
        'lastname': None,
        'notepad': None,
    }

    firstname = redis_instance.get('firstname:' + id_auth_user)
    lastname = redis_instance.get('lastname:' + id_auth_user)
    notepad = redis_instance.get('notepad:' + id_auth_user)

    if firstname and lastname and notepad:
        admin_forms_values['firstname'] = firstname.decode("utf-8")
        admin_forms_values['lastname'] = lastname.decode("utf-8")
        admin_forms_values['notepad'] = notepad.decode("utf-8")      
        return render_template('admin.html', admin_forms_values=admin_forms_values)      


def logout():
    with DB_connection() as db_connect:
        id_auth_user = request.cookies.get('flask_adminka_authorized_user_id')
        resp = Response('logout is complete')
        resp.set_cookie('flask_adminka_authorized_user_id', '', expires=0)
        return resp


def registration_tpl(password_hash, email):
    with DB_connection() as db_connect:
        db_cursor = db_connect.cursor()

        try:
            req = "insert into users(password_hash, email, active) values('" + password_hash + "', '" + email + "', 'TRUE')"
            db_cursor.execute(req)
            req = "select * from users where password_hash='" + password_hash + "' and email='" + email + "' and active=TRUE"
            db_cursor.execute(req)         
            req = "insert into options(firstname, lastname, notepad, user_id) values(NULL, NULL, NULL, '" + str(db_cursor.fetchone()[0]) + "')"
            db_cursor.execute(req)

            db_connect.commit()

            resp = Response('registered')
            return resp
        except:
            resp = Response('registration is failed')
            return resp
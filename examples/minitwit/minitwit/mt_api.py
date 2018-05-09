#This is the minitwit web api i.e. mt_api.py
import click
import time
import uuid
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime

#from flask import Flask, jsonify, request, abort

from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack,jsonify
from werkzeug import check_password_hash, generate_password_hash

#from sqlite3 import dbapi2 as sqlite3
#from minitwit import *
#from flask_basicauth import BasicAuth

#app = Flask(__name__)
# configuration
sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: buffer(u.bytes_le))

DATABASE_1 = '/tmp/minitwit1.db'
DATABASE_2 = '/tmp/minitwit2.db'
DATABASE_3 = '/tmp/minitwit3.db'

PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

# create our little application :)
app = Flask('mt_api')
app.config.from_object(__name__)
app.config.from_envvar('MT_API_SETTINGS', silent=True)


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                 for idx, value in enumerate(row))

def get_db(db_num):
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if(db_num == 0):
	if not hasattr(top, 'sqlite_db_1'):
            top.sqlite_db_1 = sqlite3.connect(app.config['DATABASE_1'], detect_types=sqlite3.PARSE_DECLTYPES)
            #top.sqlite_db.row_factory = sqlite3.Row
	    top.sqlite_db_1.row_factory = make_dicts
            return top.sqlite_db_1
    elif(db_num == 1):
        if not hasattr(top, 'sqlite_db_2'):
            top.sqlite_db_2 = sqlite3.connect(app.config['DATABASE_2'], detect_types=sqlite3.PARSE_DECLTYPES)
	    top.sqlite_db_2.row_factory = make_dicts
            return top.sqlite_db_2
    elif(db_num == 2):
        if not hasattr(top, 'sqlite_db_3'):
            top.sqlite_db_3 = sqlite3.connect(app.config['DATABASE_3'], detect_types=sqlite3.PARSE_DECLTYPES)          
            top.sqlite_db_3.row_factory = make_dicts
            return top.sqlite_db_3
    else:
        top.sqlite_db_1 = sqlite3.connect(app.config['DATABASE_1'], detect_types=sqlite3.PARSE_DECLTYPES)
        top.sqlite_db_1.row_factory = make_dicts
        top.sqlite_db_2 = sqlite3.connect(app.config['DATABASE_2'], detect_types=sqlite3.PARSE_DECLTYPES)
        top.sqlite_db_2.row_factory = make_dicts
        top.sqlite_db_3 = sqlite3.connect(app.config['DATABASE_3'], detect_types=sqlite3.PARSE_DECLTYPES)
        top.sqlite_db_3.row_factory = make_dicts
    return top.sqlite_db_1, top.sqlite_db_2, top.sqlite_db_3

@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db_1'):
        top.sqlite_db_1.close()
        #top.sqlite_db_2.close()
        #top.sqlite_db_3.close()
    if hasattr(top, 'sqlite_db_2'):
        #top.sqlite_db_1.close()
        top.sqlite_db_2.close()
        #top.sqlite_db_3.close()
    if hasattr(top, 'sqlite_db_3'):
        #top.sqlite_db_1.close()
        #top.sqlite_db_2.close()
        top.sqlite_db_3.close()
    #else:
        #top.sqlite_db_1.close()
        #top.sqlite_db_2.close()
        #top.sqlite_db_3.close()

def init_db():
    """Initializes the database."""
    #db = get_db()
    #with app.open_resource('schema.sql', mode='r') as f:
        #db.cursor().executescript(f.read())
    #db.commit()
    db_connections = get_db(4)
    for db in db_connections:
        with app.open_resource('schema_shard.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    db_connections = get_db(4)
    for db in db_connections:
        #cur = get_db(4).execute(query, args)
        cur = db.execute(query, args)
        rv = cur.fetchall()
        #rv.append(result)
    return (rv[0] if rv else None) if one else rv


def populate_db():
    # Populates the database
    #db = get_db(4)
    db_connections = get_db(4)
    for db in db_connections:
        with app.open_resource('population_shard.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('populatedb')
def populatedb_command():
    #Populates the database
    populate_db()
    print('Populated the database.')

@app.route('/api/v1.0/mt', methods=['GET'])
def get_tasks():
    return jsonify({'task': "hello world!!!"})

@app.route('/api/v1.0/resources/users/<username>', methods=['GET'])
def user_id(username):
    print('llllllllll')
    query = '''SELECT user_id FROM user WHERE username = "{}"'''.format(username)
    result = query_db(query)
    print('result:{}'.format(result))
    print(type(result))
    if not result:
        return jsonify({'uID': None})
	
    userID_dict = result[0]
    uID = userID_dict['user_id']
    print(uID)
    return jsonify({'uID': uID})

@app.route('/api/v1.0/resources/messages_add/<author_id>', methods=['POST'])
def add_message(author_id):
     """Registers a new message for the user."""
     print('BBBBBBBBBBBBBBBBBBBBBBBBbb')
     #if not request.json or not 'author_id' in request.json or not 'text' in request.json:
     if not request.json or not 'text'in request.json:
         abort(401)
     db_num = dbnumber(author_id)
     db = get_db(db_num)
     text = request.json.get('text')
     pub_date =int(time.time())
     #print(text)
     db.execute('''insert into message (author_id, text, pub_date) values (?, ?, ?)''',
                (author_id, text, pub_date))
     db.commit()
     return jsonify("message stored: sucessessful"), 201 


@app.route('/api/v1.0/resources/user', methods=['POST'])
def before_request():
    print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
    user_id = request.json.get('user_id')
    g.user = query_db('select * from user where user_id = ?',[user_id], one=True)
    print('g.user:{}'.format(g.user))
    return jsonify({'g.user': g.user}) 



@app.route('/api/v1.0/resources/', methods=['POST'])
def timeline():
    print('//////////////////////////')
    user_id = request.json.get('user_id')
    messages=query_db('''select message.*, user.* from message, user where message.author_id = user.user_id and (user.user_id = ? or user.user_id in (select whom_id from follower where who_id = ?))order by message.pub_date desc limit ?''',[user_id, user_id, PER_PAGE])
    return jsonify({'messages':messages})



@app.route('/api/v1.0/resources/timeline/public', methods=['GET'])
def public_timeline():
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    messages=query_db('''select message.*, user.* from message, user where message.author_id = user.user_id order by message.pub_date desc limit ?''', [PER_PAGE])
    return jsonify({'messages':messages})


@app.route('/api/v1.0/resources/users/<user_id>/follow', methods=['POST'])
def user_follow(user_id):
    db_num = dbnumber(user_id)
    db = get_db(db_num)
    whom_id = request.json.get('whom_id')
    db.execute('insert into follower(who_id,whom_id) values (?,?)',[user_id, whom_id])
    db.commit() 
    return jsonify("followed successful"),201


@app.route('/api/v1.0/resources/timeline/<username>', methods=['POST'])
def user_timeline(username):
    user_id = request.json.get('user_id')
    print('user_id:{}'.format(user_id))
    print('username:{}'.format(username))
    profile_user = query_db('select * from user where username = ?', [username], one=True)
    #followed = False
    print('profile_user:{}'.format(profile_user))
    followed = query_db('''select 1 from follower where follower.who_id = ? and follower.whom_id = ?''', [user_id, profile_user['user_id']], one=True) is not None
    print(followed)
    if followed is None:
        followed = False
    #else:
        #followed = True
    messages = query_db('''select message.*, user.* from message, user where user.user_id = message.author_id and user.user_id = ? order by message.pub_date desc limit ?''',[profile_user['user_id'], PER_PAGE] )
    return jsonify({'profile_user': profile_user, 'messages': messages, 'followed': followed})


@app.route('/api/v1.0/resources/users/<user_id>/unfollow', methods=['POST'])
def user_unfollow(user_id):
    db_num = dbnumber(user_id)
    db = get_db(db_num)
    whom_id = request.json.get('whom_id')
    db.execute('delete from follower where who_id=? and whom_id=?', [user_id,whom_id])
    db.commit()
    return jsonify("unfollowed successful"),201


@app.route('/api/v1.0/resources/users/login/<username>', methods=['GET'])
def login(username):
    print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
    user = query_db('''select * from user where username = "{}"'''.format(username))
    print('99999999999999999999user :{}'.format(user))
    return jsonify({'user':user})


def dbnumber(user_id):
    return int(int(user_id) % 3)

@app.route('/api/v1.0/register', methods=['POST'])
def register():
    """Registers the user."""
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'pw_hash' in request.json:
        abort(400)
    u = uuid.uuid4()
    db_num = dbnumber(u)
    db = get_db(db_num)
    entry = {
        'user_id':u,
        'username': request.json.get('username'),
        'email': request.json.get('email'),
        'pw_hash': request.json.get('pw_hash')
    }

    db.execute('''insert into user (
             user_id, username, email, pw_hash) values (?, ?, ?, ?)''',(entry['user_id'],entry['username'], entry['email'],entry['pw_hash']))
    db.commit()
   # flash('Your have been registered')

   # return jsonify({'mt':entry}), 201
    return jsonify("its success"), 201

if __name__=='__main__':
    app.run(debug=true)
    #app.run(host='127.0.0.1',port=5001,debug=True)

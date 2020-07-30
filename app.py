# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import request
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
load_dotenv()
import datetime
from bson.objectid import ObjectId
from flask import session 
import bcrypt

# -- Initialization section --
app = Flask(__name__)
app.jinja_env.globals['current_time'] = datetime.datetime.now()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
MONGO_DBNAME = os.getenv("MONGO_DBNAME")
MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
app.config['MONGO_DBNAME'] = MONGO_DBNAME
app.config['MONGO_URI'] = f'mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@cluster0.udw0r.mongodb.net/{MONGO_DBNAME}?retryWrites=true&w=majority'
print(app.config["MONGO_URI"])
mongo = PyMongo(app)

# -- Routes section --
# INDEX
@app.route('/')
@app.route('/index')
def index():
    data = {
    }
    return render_template('index.html', data=data)

@app.route('/add', methods=['GET','POST'])
def events_add():
    if request.method == 'GET':
        data = {
        }
        return render_template('eventsAdd.html', data=data)
    else:
        ## Add event to events_list
        form = request.form
        event = {
        'name':form['eventName'],
        'date':form['eventDate'],
        'user':form['eventUser'],
        'eventDescription': form['eventDescription'],
        'userAccount': session['email']
        }
        events = mongo.db['events-list']
        events.insert(event)
        return redirect(url_for('events_cal'))
    
@app.route('/eventscal')
def events_cal():
    #All Jan events
    jan_events = mongo.db['events-list'].find({"date": {'$regex':"-01-"}}).sort('date')
    #All Feb events
    feb_events = mongo.db['events-list'].find({"date": {'$regex':"-02-"}}).sort('date') 
    #All Mar events
    mar_events = mongo.db['events-list'].find({"date": {'$regex':"-03-"}}).sort('date')
    #All Apr events
    apr_events = mongo.db['events-list'].find({"date": {'$regex':"-04-"}}).sort('date')
    #All May events
    may_events = mongo.db['events-list'].find({"date": {'$regex':"-05-"}}).sort('date')
    #All Jun events
    jun_events = mongo.db['events-list'].find({"date": {'$regex':"-06-"}}).sort('date')
    #All Jul events
    jul_events = mongo.db['events-list'].find({"date": {'$regex':"-07-"}}).sort('date')
    #All Aug events
    aug_events = mongo.db['events-list'].find({"date": {'$regex':"-08-"}}).sort('date')
    #All Sep events
    sep_events = mongo.db['events-list'].find({"date": {'$regex':"-09-"}}).sort('date')
    #All Oct events
    oct_events = mongo.db['events-list'].find({"date": {'$regex':"-10-"}}).sort('date')
    #All Nov events
    nov_events = mongo.db['events-list'].find({"date": {'$regex':"-11-"}}).sort('date') 
    #All Dec events
    dec_events = mongo.db['events-list'].find({"date": {'$regex':"-12-"}}).sort('date')
    #events = mongo.db['events-list'].find({}) 
    data = {
    'jan_events':mongo.db['jan_events'].find({'userAccount': session['email']}),
    'feb_events':mongo.db['feb_events'].find({'userAccount': session['email']}),
    'mar_events':mongo.db['mar_events'].find({'userAccount': session['email']}),
    'apr_events':mongo.db['apr_events'].find({'userAccount': session['email']}),
    'may_events':mongo.db['may_events'].find({'userAccount': session['email']}),
    'jun_events':mongo.db['jun_events'].find({'userAccount': session['email']}),
    'jul_events':mongo.db['jul_events'].find({'userAccount': session['email']}),
    'aug_events':mongo.db['aug_events'].find({'userAccount': session['email']}),
    'sep_events':mongo.db['sep_events'].find({'userAccount': session['email']}),
    'oct_events':mongo.db['oct_events'].find({'userAccount': session['email']}),
    'nov_events':mongo.db['nov_events'].find({'userAccount': session['email']}),
    'dec_events':mongo.db['dec_events'].find({'userAccount': session['email']})
    }
    print(data)
    return render_template('familycalendar.html', data=data)
    
@app.route('/remove', methods=['GET','POST'])
def events_remove():
    if request.method == 'GET':
        data = {}
        return render_template('eventRemove.html', data=data)
    else:
        events = mongo.db['events-list']
        form = request.form
        eventName = request.form['eventName']
        eventDate = request.form['eventDate']
        eventName_dict = {'name':eventName}
        eventDate_dict = {'date':eventDate}
        events.delete_one(eventName_dict)
        events.delete_one(eventDate_dict)
        events = mongo.db['events-list'].find({'userAccount': session['email']})
        return redirect(url_for('events_cal'))

@app.route('/users')
def users_view():
    data = {
    'users':mongo.db['users'].find({'userAccount': session['email']})
    }
    print(data)
    return render_template('userView.html', data=data)

@app.route('/users/add', methods=['GET','POST'])
def users_add():
    if request.method == 'GET':
        data = {
        }
        return render_template('userAdd.html', data=data)
    else:
        form = request.form
        user = {
            "userName": form["userName"],
            "userAge": form["userAge"],
            "userPhone": form["userPhone"],
            "userWork": form["userWork"],
            "userHobbies": form["userHobbies"],
            'userAccount': session['email']
        }
        users = mongo.db['users']
        users.insert_one(user)
        return redirect(url_for('users_view'))

@app.route('/chores/add', methods=['GET','POST'])
def chores_add():
    if request.method == 'GET':
        data = {
        }
        return render_template('choreAdd.html', data=data)
    else:
        form = request.form
        chore = {
            "choreType": form["choreType"],
            "choreName": form["choreName"],
            "choreInputter": form["choreInputter"],
            'userAccount': session['email']
        }
        chores = mongo.db['chores']
        chores.insert_one(chore)
        return redirect(url_for('chores_view'))

@app.route('/chores')
def chores_view():
    #All Bedroom Chores
    bedroom_chores = mongo.db['chores'].find({"choreType": {'$regex':"Bedroom"}}).sort('choreType')
    #All Kitchen Chores
    kitchen_chores = mongo.db['chores'].find({"choreType": {'$regex':"Kitchen"}}).sort('choreType')
    #All Bathroom Chores
    bathroom_chores = mongo.db['chores'].find({"choreType": {'$regex':"Bathroom"}}).sort('choreType')
    #All Outside Chores
    outside_chores = mongo.db['chores'].find({"choreType": {'$regex':"Outside"}}).sort('choreType')
    #All Meal Chores
    meal_chores = mongo.db['chores'].find({"choreType": {'$regex':"Meal"}}).sort('choreType')
    #All Miscellaneous Chores
    miscell_chores = mongo.db['chores'].find({"choreType": {'$regex':"Miscellaneous"}}).sort('choreType')
    data = {
    'bedroom_chores':mongo.db['bedroom_chores'].find({'userAccount': session['email']}),
    'kitchen_chores':mongo.db['kitchen_chores'].find({'userAccount': session['email']}),
    'outside_chores':mongo.db['outside_chores'].find({'userAccount': session['email']}),
    'meal_chores':mongo.db['meal_chores'].find({'userAccount': session['email']}),
    'miscell_chores':mongo.db['miscell_chores'].find({'userAccount': session['email']}),
    }
    return render_template('choresView.html', data=data)


@app.route('/photos')
def photos_view():
    photos=[""]
    data = {
        "photos": photos
    }
    return render_template('photoView.html',data=data)

@app.route('/chores/complete', methods=['GET','POST'])
def chores_complete():
    if request.method == 'GET':
        return redirect(url_for('chores_view'))
    else:
        form = request.form
        choreid = form['choreid']
        choreid = ObjectId(choreid) 
        query = {
            '_id':choreid
        }
        update = {
            '$set': {'Completed':form.get('Completed',"")}
        }
        mongo.db['chores'].find_one_and_update(query, update)
        return redirect(url_for('chores_view'))

@app.route('/messages')
def message_view():
    data = {
    'messages':mongo.db['messages'].find({})
    }
    return render_template('messageView.html', data=data)


@app.route('/messages/add', methods=['GET','POST'])
def message_add():
    if request.method == 'GET':
        data = {
        }
        return render_template('messageAdd.html', data=data)
    else:
        form = request.form
        message = {
            "userName": form["userName"],
            "message": form["message"],
        }
        messages = mongo.db['messages']
        messages.insert_one(message)
        return redirect(url_for('message_view'))

@app.route('/auth/signup', methods=['GET','POST'])
def auth_signup():
    if request.method == 'GET':
        data = {
        }
        return render_template('auth/signup.html', data=data)
    else:
        form = request.form
        user = {
            "email": form["email"],
        }
        document= mongo.db['information'].find_one(user)
        if document is None:
            password = form['password']
            hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user['password'] = str(hashpass, 'utf-8')
            mongo.db['information'].insert(user)
            session['email'] = form['email']
            return redirect(url_for("index"))
        else: 
            return redirect(url_for('auth_signup'))


@app.route('/auth/login', methods=['GET','POST'])
def auth_login():
    if request.method == 'GET':
        data = {
        }
        return render_template('auth/login.html', data=data)
    else:
        form = request.form
        user = {
            "email": form["email"],
        }
        document= mongo.db['information'].find_one(user)
        if document is not None and session.get('username') is None:
            password = form['password']
            if bcrypt.checkpw(password.encode('utf-8'), document['password'].encode('utf-8')):
                session['email'] = form['email']
                return redirect(url_for("index"))
            else:
                return "The username or password is incorrect."
        else: 
            return redirect(url_for('auth_signup'))


@app.route('/auth/logout')
def auth_logout():
    session.clear()
    return redirect(url_for('index'))
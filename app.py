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



# -- Initialization section --
app = Flask(__name__)
app.jinja_env.globals['current_time'] = datetime.datetime.now()


events = [
        {"name":"First Day of Classes", "date":"2020-08-21"},
        {"name":"Winter Break", "date":"2020-12-20"},
        {"name":"Finals Begin", "date":"2020-12-01"}
    ]

MONGO_DBNAME = os.getenv("MONGO_DBNAME")
MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")

app.config['MONGO_DBNAME'] = MONGO_DBNAME
app.config['MONGO_URI'] = f'mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@cluster0.udw0r.mongodb.net/{MONGO_DBNAME}?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')
def index():
    data = {
    'events':events,
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
        'user':form['eventUser']
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
    'jan_events':jan_events,
    'feb_events':feb_events,
    'mar_events':mar_events,
    'apr_events':apr_events,
    'may_events':may_events,
    'jun_events':jun_events,
    'jul_events':jul_events,
    'aug_events':aug_events,
    'sep_events':sep_events,
    'oct_events':oct_events,
    'nov_events':nov_events,
    'dec_events':dec_events
    }
    return render_template('familycalendar.html', data=data)

@app.route('/users')
def users_view():
    data = {
    'user':mongo.db['user'].find({})
    }
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
        'firstName': form['firstName'],
        'lastName': form['lastName'],
        'username': form['username'],
        'city': form['city'],
        'state': form['state'],
        'zip': form['zipCode']
        }
        users = mongo.db['users']
        users.insert_one(user)

        return redirect(url_for('users'))



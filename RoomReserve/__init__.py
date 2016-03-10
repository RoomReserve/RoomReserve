import os, sys, time
from flask import *
from jinja2 import Template
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import *
from wtforms.validators import *
from flask_wtf import Form, validators
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from datetime import datetime
import delorean
from delorean import Delorean
import RoomReserve.helpers.delorean_helper as delorean_helper


#RoomReserve constant variables
import RoomReserve.helpers.constant_variables as CONST


# flask-heroku
from flask.ext.heroku import Heroku

# flask-login
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required

#these are imported for the engine and session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Start flask instance
app = Flask(__name__)
app.secret_key = 'x95xe1gxceHGxeaSx0exf5xf4xbaxb5x1dxe5'

heroku = Heroku(app)
db = SQLAlchemy(app)

# FLASK-LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




# DATABASE SELECTION
def set_database():
	'''
	Uses a temporary database if the program detects that
	it is running on a mac, otherwise it uses the production
	database on Heroku postgres.
	'''
	if sys.platform == 'darwin':
		# running on a mac
		DATABASE_URL = "sqlite:////tmp/tempdb_rr.db"
	else:
		# heroku postgresql database
		DATABASE_URL = "postgres://cypesbhdqdjwdm:_Fc_oDYnfvYp8Ma5F3aOnJMHXd@ec2-54-83-17-9.compute-1.amazonaws.com:5432/d5r02un6qtqh6h"


	app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

set_database()

from RoomReserve.helpers.render import render



#DatabaseTables
from RoomReserve.dbtables.user import User
from RoomReserve.dbtables.guest import Guest
from RoomReserve.dbtables.building import Building
from RoomReserve.dbtables.room import Room
from RoomReserve.dbtables.reservation import Reservation

#RoomReserve modules
import RoomReserve.helpers.login as Login
import RoomReserve.homepage
import RoomReserve.helpers.errorhandlers
import RoomReserve.admin.admin
import RoomReserve.admin.user
import RoomReserve.admin.building
import RoomReserve.admin.rooms
import RoomReserve.admin.guest
import RoomReserve.admin.reservation
import RoomReserve.reservationwizard
import RoomReserve.admin.guestsearch
import RoomReserve.admin.dashboard
import RoomReserve.admin.mainSearch
import RoomReserve.newguest
# Creates database classes as defined in the
# above imports from RoomReserve.dbtables.*
db.create_all()
db.session.commit()



def createDefaultAccounts():
	'''
	Creates an account of each role for testing purposes.
	'''

	defaultAdmins = []
	for me in db.session.query(User).filter_by(email='admin@localhost'):
		defaultAdmins.append(me)
	if len(defaultAdmins) > 0:
		#default admin is already created
		print("Default admin account admin@localhost exists.")
	else:
		admin = User('Default pw is rr', 'Admin', 'admin@localhost', 'admin', 'rr')

		standard = User('Default pw is rr', 'Standard', 'standard@localhost', 'standard', 'rr')

		readonly = User('Default pw is rr', 'Readonly', 'ro@localhost', 'readonly', 'rr')

		inactive = User('Default pw is rr', 'Inactive', 'inactive@localhost', 'inactive', 'rr')

		db.session.add(admin)
		db.session.add(standard)
		db.session.add(readonly)
		db.session.add(inactive)
		db.session.commit()
		print("Default admin account 'admin@localhost' created. Welcome to RoomReserve.")


createDefaultAccounts()


def createSampleGuests():
	'''
	Create few guest users for testing purposes
	'''

	sampleGuests = []
	for g in db.session.query(Guest).filter_by(email='i.newton@gmail.com'):
		sampleGuests.append(g)
	if len(sampleGuests) > 0:
		print('Sample guest account i.newton@gmail.com exists.')
	else:
		guest1 = Guest(first='Isaac', last='Newton', email='i.newton@gmail.com', phone='523-343-4545', address='Iowa City, Iowa', payment=45, notes="Paid")
		guest2 = Guest(first='Bruce', last='Lee', email='b.lee@gmail.com', phone='454-999-3334', address='Chicago, Illinois', payment=5000, notes="Paid")

		db.session.add(guest1)
		db.session.add(guest2)
		db.session.commit()
		print("Sample guests added.")


createSampleGuests()


def createSampleBuildings():
	'''
	Create sample buildings for testing purposes
	'''

	sampleBuildings = []
	for b in db.session.query(Building).filter_by(name='Miller Hall'):
		sampleBuildings.append(b)
	if len(sampleBuildings) > 0:
		print('Sample building exists.')
	else:
		miller = Building(name='Miller Hall', numfloors=8, status=CONST.ready_status, description="Corner rooms are bigger", notes="")
		brandt = Building(name='Brandt Hall', numfloors=5, status=CONST.ready_status, description="First years only", notes="")
		ylvi = Building(name='Ylvisaker Hall', numfloors=4, status=CONST.ready_status, description="First years only", notes="")		
		db.session.add(miller)
		db.session.add(brandt)
		db.session.add(ylvi)
		db.session.commit()
		print("Sample buildings added.")


createSampleBuildings()


def createSampleRooms():
	'''
	Create sample rooms for testing purposes
	'''

	sampleRooms = []
	for b in db.session.query(Room).filter_by(roomnumber = '401'):
		sampleRooms.append(b)
	if len(sampleRooms) > 0:
		print('Sample room exists.')
	else:
		m401 = Room(roomnumber='401', buildingID='1', capacity='2', description="Corner Rooms are bigger",  status=CONST.ready_status, notes="")
		b202 = Room(roomnumber='202', buildingID='2', capacity='4', description="First Years Only", status=CONST.occupied_status, notes="")
		yl319 = Room(roomnumber='319', buildingID='3', capacity='2', description="First Years Only", status=CONST.inactive_status, notes="")
		db.session.add(m401)
		db.session.add(b202)
		db.session.add(yl319)
		db.session.commit()
		print("Sample rooms added.")


createSampleRooms()


# Try not to add additional page routes in here.

@app.route("/dbtest")
def db_test():
	title = sys.platform
	users = User.query.all()
	return render_template('test.html', title=title, users=users)

class test_form(Form):
	name = StringField('Name', validators=[DataRequired()])

@app.route("/wtftest", methods=['GET', 'POST'])
def wtf_test():
	if request.method == 'GET':
		form = test_form()
		return render_template('formtest.html', form=form)
	elif request.method == 'POST':
		content = "hello "
		content += request.form['name']
		return render_template('basic.html', content=content)
	else:
		return RoomReserve.helpers.errorhandlers.page_error400(400)

@app.route("/today")
def page_today():
	title="Today's Activity"
	return render('today.html',title=title)



@app.route('/droptables', methods=['GET', 'POST'])
def droptables():
	# Drops all the data we have currently.
	deleteAll_Password = 'deleteall'
	deleteAll_ExceptUsers = 'delete'


	if request.method == 'POST' and request.form['verify'] == deleteAll_Password:
		db.drop_all()
		db.create_all()
		createDefaultAccounts()
		createSampleGuests()
		createSampleBuildings()
		createSampleRooms()
		print("TABLES REBUILT")
		return render('basic.html',title="Tables erased.",content="Data has been reset")

	elif request.method == 'POST' and request.form['verify'] == deleteAll_ExceptUsers:
		db.drop_all(bind=Reservation)
		db.create_all()
		createDefaultAccounts()
		print("TABLES REBUILT")
		return render('basic.html',title="Tables erased.",content="SOME data has been reset")

	else:
		content = 'Type the password to verify. <form action="/droptables" method="POST">'
		content += '<input type="text" name="verify">'
		content += '<input type="submit" value="Delete All Data">'
		return render('basic.html',title="Drop Table Verification",content=content)

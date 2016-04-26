import os, sys, time
from flask import *
from jinja2 import Template
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import *
from wtforms.validators import *
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, StringField, SubmitField, validators
from flask import Flask, render_template, flash, request, url_for
from datetime import datetime
from datetime import date, timedelta
import delorean
from delorean import Delorean
import RoomReserve.helpers.delorean_helper as delorean_helper
import time
import traceback
# from flask.ext.moment import Moment



# momentjs for timestamp
import RoomReserve.helpers.momentjs


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
# moment = Moment(app)
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
import RoomReserve.admin.homepage
import RoomReserve.helpers.errorhandlers
import RoomReserve.admin.admin
import RoomReserve.admin.user
import RoomReserve.admin.building
import RoomReserve.admin.rooms
import RoomReserve.admin.guest
import RoomReserve.admin.reservation
import RoomReserve.admin.reservationwizard
import RoomReserve.admin.guestsearch
import RoomReserve.admin.dashboard
import RoomReserve.admin.mainSearch
import RoomReserve.admin.checkinout
import RoomReserve.admin.newguest
import RoomReserve.helpers.stats as stats


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
		admin = User('Default', 'Admin', 'admin@localhost', 'admin', 'rr')

		dd = User('Dorjee', 'Dhondup', 'dhondup@luther.edu', 'admin', 'dd')

		standard = User('Default', 'Standard', 'standard@localhost', 'standard', 'rr')

		readonly = User('Default', 'Readonly', 'ro@localhost', 'readonly', 'rr')

		inactive = User('Default', 'Inactive', 'inactive@localhost', 'inactive', 'rr')

		db.session.add(admin)
		db.session.add(dd)
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

@app.route("/createtestrooms")
def page_createtestrooms():
	r=[]
	r.append(Room(roomnumber='402', buildingID='1', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='403', buildingID='1', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='404', buildingID='1', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='405', buildingID='1', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='406', buildingID='1', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='407', buildingID='1', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='408', buildingID='1', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='409', buildingID='1', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='130', buildingID='2', capacity='3', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='132', buildingID='2', capacity='3', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='134', buildingID='2', capacity='3', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='136', buildingID='2', capacity='3', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='138', buildingID='2', capacity='3', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='140', buildingID='2', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='142', buildingID='2', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='201', buildingID='3', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='203', buildingID='3', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='205', buildingID='3', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='207', buildingID='3', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='209', buildingID='3', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='211', buildingID='3', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='213', buildingID='3', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='215', buildingID='3', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='217', buildingID='3', capacity='2', description="",  status=CONST.ready_status, notes=""))
	r.append(Room(roomnumber='499', buildingID='2', capacity='8', description="Fairy-Tale Suite", status=CONST.ready_status, notes=""))

	for me in r:
		db.session.add(me)
	db.session.commit()

	return redirect(url_for("page_rooms"))

@app.route('/beveryverycareful')
def page_create_all():
	try:
		db.drop_all()
		db.create_all()
		createDefaultAccounts()
		
		db.session.add(Building(name="Miller", numfloors=8, status=CONST.ready_status, description="Contains numerous two person rooms and two elevators.", notes="This building is available for the summer."))
		db.session.add(Building(name="Dieseth", numfloors=8, status=CONST.ready_status, description="Contains numerous two person rooms and a single elevator.", notes="This building is available for the summer."))
		db.session.add(Building(name="Brandt", numfloors=5, status=CONST.ready_status, description="First year hall that has both three person and two person rooms.", notes="This building is used for parents for graduation and some camps."))
		db.session.add(Building(name="Farwell", numfloors=8, status=CONST.ready_status, description="Rooms are set up and organized around central rooms.", notes="This building is available for the summer school students."))
		db.session.add(Building(name="Larsen", numfloors=4, status=CONST.inactive_status, description="Larsen has heaters in each room and contains a wardrobe in each room as well.", notes="This building is unavailable."))
		db.session.add(Building(name="Ylvisaker", numfloors=5, status=CONST.ready_status, description="First year hall that has numerous two person rooms. The hallways are a bit smaller here.", notes="This building is available for the summer."))
		db.session.add(Building(name="Olson", numfloors=3, status=CONST.ready_status, description="Olson has many two person rooms and suites that are two person rooms with a central room between those two.", notes="This building is available for the summer."))
		db.session.commit()
		for j in range(1, 16):
			db.session.add(Room(roomnumber= j, buildingID='3', capacity='2', description="Room in Brandt",  status=CONST.ready_status, notes="Groud Floor"))
		for i in range(1, 9):
			for j in range(1, 31):
				db.session.add(Room(roomnumber=(i * 100 + j), buildingID='1', capacity='2', description="Room in Miller",  status=CONST.ready_status, notes=""))
				db.session.add(Room(roomnumber=(i * 100 + j), buildingID='2', capacity='2', description="Room in Dieseth",  status=CONST.ready_status, notes=""))
				db.session.add(Room(roomnumber=(i * 100 + j), buildingID='4', capacity='2', description="Room in Farwell",  status=CONST.ready_status, notes=""))
				if i < 5:
					db.session.add(Room(roomnumber=(i * 100 + j), buildingID='3', capacity='2', description="Room in Brandt",  status=CONST.ready_status, notes=""))
					db.session.add(Room(roomnumber=(i * 100 + j + 30), buildingID='3', capacity='3', description="Room in Brandt",  status=CONST.ready_status, notes="Three person room"))
					db.session.add(Room(roomnumber=(i * 100 + j), buildingID='5', capacity='2', description="Room in Larsen",  status=CONST.inactive_status, notes=""))
					if i != 4:
						db.session.add(Room(roomnumber=(i * 100 + j), buildingID='7', capacity='4', description="Room in Olson",  status=CONST.ready_status, notes=""))
					db.session.add(Room(roomnumber=(i * 100 + j), buildingID='6', capacity='2', description="Room in Ylvi",  status=CONST.ready_status, notes=""))
					
		db.session.commit()
		fnlist = ["Bruce", "Tom", "Harry", "David", "Henry", "Thomas", "Isaac", "Katie", "Susan", "Peter", "Kelly", "Emilay", "Alahna", "Morgan", "Neil", "Kierra", "Leah", "Lucia", "Marissa", "Melissa", "Aidan"]
		lnlist = ["Bennett", "Dhondup", "Stekel", "Miller", "Lee", "Ranum", "Newton", "Smith", "Brown", "Davidson", "Robinson", "Schroeder", "Keil", "Mortenson", "Anderson", "Blackstad", "Williams", "Holte", "Wales", "Hrdlicka", "Cook"]
		hatlist = ["Beanie", "Coonskin Hat", "Top Hat", "Sombrero", "Trucker Hat"]
		for i in range(0, len(fnlist)):
			for j in range(0, len(lnlist)):
				db.session.add(Guest(fnlist[i], lnlist[j], lnlist[j][:4].lower() + fnlist[i][:2].lower() + "01@luther.edu", "563" + "-" + str(495-i*7) + "-" + str(9321 - j*17),  str(i*100 + j * 10 + j%10) + " College Drive, Decorah IA", payment=(i * 10 + j), notes="Wears a " + hatlist[i%len(hatlist)]))
		#still need to add reservations
		
		db.session.commit()
		
		from RoomReserve.Admin.rooms import getRoomByID
		
		myiter = 0
		for i in range(1, len(fnlist)*len(lnlist)):
			#change the month below to 5 for when we present
			myiter += 1
			while getRoomByID(myiter).status == CONST.inactive_status:
				myiter += 1
				
			x = int(i%30+1)
			mydate = date(2016, 4, x)
			mydate2 = mydate + timedelta(days=(i%30))
			if datetime.today().date() < mydate:
				mystatus = CONST.ready_status
			else:
				if datetime.today().date() < mydate2:
					mystatus = CONST.checkedin_status
					getRoomByID(myiter).set_status(CONST.occupied_status)
				else:
					mystatus = CONST.checkedout_status
					getRoomByID(myiter).set_status(CONST.unclean_status)
			db.session.add(Reservation(i , 1, myiter, mydate, mydate2, mystatus, "Beds need lofting."))
			
		db.session.commit()
		return redirect(url_for("page_rooms"))
	except:
		print("Hit the except statement")
		return render("basic.html", content=str(traceback.format_exc()).replace('\n', '<br>'))
		



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

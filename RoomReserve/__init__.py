from flask import *
from jinja2 import Template
from flask.ext.sqlalchemy import SQLAlchemy

#Start flask instance
app = Flask(__name__)
app.secret_key = 'x95xe1gxceHGxeaSx0exf5xf4xbaxb5x1dxe5'

#RoomReserve modules
import RoomReserve.helpers.session
import RoomReserve.homepage
import RoomReserve.helpers.errorhandlers


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

# User
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first = db.Column(db.String(40), unique=False)
	last = db.Column(db.String(40), unique=False)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(100), unique=False)
	role = db.Column(db.String(100), unique=False)

	def __init__(self, first, last, email, role, password="helloworld"):
		self.first = first
		self.last = last
		self.email = email
		self.role = role
		self.password = password

	def __repr__(self):
		return '%r %r' % (self.first, self.last)
class Guest(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first = db.Column(db.String(40), unique=False)
	last = db.Column(db.String(40), unique=False)
	email = db.Column(db.String(50), unique=True)
	phone = db.Column(db.Integer, unique=False)
	address = db.Column(db.String(75), unique=False)
	payment = db.Column(db.Integer, unique=False)
	notes = db.Column(db.String(500), unique=False)
	

	def __init__(self, first, last, email, phone, address, payment, notes=""):
		self.first = first
		self.last = last
		self.email = email
		self.phone = phone
		self.address = address
		self.payment = payment
		self.notes = notes

	def __repr__(self):
		return '%r %r' % (self.first, self.last)

class Reservation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	guest = db.Column(db.Integer, ForeignKey("Guest.id"), nullable=False)
	madeby = db.Column(db.Integer, ForeignKey("User.id"), nullable=False)
	place = db.Column(db.Integer, ForeignKey("Room.id"), nullable=False)
	time = db.Column(datetime.datetime, nullable=False, unique=False)
	status = db.Column(db.String(20), unique=False, nullable=False)
	notes = db.Column(db.String(500), unique=False)

	def __init__(self, guest, madeby, place, time, status="Unarrived", notes=""):
		self.guest = guest
		self.madeby = madeby
		self.place = place
		self.time = time
		self.status = status
		self.notes = notes

	def __repr__(self):
		return '%r %r' % (self.time, self.place)
		
class Room(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	roomnumber = db.Column(db.Integer, unique=False, nullable=True)
	building = db.Column(db.String(30), unique=False, nullable=False)
	floor = db.Column(db.Integer, unique=False, nullable=True)
	capacity = db.Column(db.Integer, unique=False, nullable=True)
	description = db.Column(db.String(500), unique=False)
	status = db.Column(db.String(20), unique=False, nullable=False)
	notes = db.Column(db.String(500), unique=False)

	def __init__(self, roomnumber, floor, building, capacity, description="", status="Ready", notes=""):
		self.roomnumber = roomnumber
		self.building = building
		self.floor = floor
		self.capacity = capacity
		self.description = description
		self.status = status
		self.notes = notes

	def __repr__(self):
		return '%r %r %r' % (self.roomnumber, self.floor, self.bullding)

db.create_all()

admin = User('Dorjee', 'Dhondup', 'dhondo01@luther.edu', 'admin')
admin2 = User('Ryan', 'Bennett', 'bennry01@luther.edu', 'admin')
admin3 = User('Zach', 'Stakel', 'dsfd@luther.edu', 'admin')

db.session.add(admin)
db.session.add(admin2)
db.session.add(admin3)

db.session.commit()

users = User.query.all()



@app.route("/dbtest")
def db_test():
    title = "DB Works!"
    return render_template('test.html', title=title, users=users)


@app.route("/today")
def page_today():
	title="Today's Activity"
	return render_template('basic.html',title=title)

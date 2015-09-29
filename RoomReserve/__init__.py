from flask import *
from jinja2 import Template
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
import RoomReserve.homepage
import RoomReserve.helpers.errorhandlers


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

# User
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first = db.Column(db.String(100), unique=False)
	last = db.Column(db.String(100), unique=False)
	email = db.Column(db.String(100), unique=True)
	role = db.Column(db.String(100), unique=False)

	def __init__(self, first, last, email, role):
		self.first = first
		self.last = last
		self.email = email
		self.role = role

	def __repr__(self):
		return '%r %r' % (self.first, self.last)


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

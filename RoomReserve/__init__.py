from flask import *
from jinja2 import Template
from flask.ext.sqlalchemy import SQLAlchemy

#Start flask instance
app = Flask(__name__)
app.secret_key = 'x95xe1gxceHGxeaSx0exf5xf4xbaxb5x1dxe5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)


#RoomReserve modules
import RoomReserve.helpers.session
import RoomReserve.homepage
import RoomReserve.helpers.errorhandlers
from RoomReserve.dbtables.user import User









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

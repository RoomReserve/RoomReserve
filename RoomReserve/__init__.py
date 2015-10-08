from flask import *
from jinja2 import Template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import *
from wtforms.validators import *

#these are imported for the engine and session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Start flask instance
app = Flask(__name__)
app.secret_key = 'x95xe1gxceHGxeaSx0exf5xf4xbaxb5x1dxe5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test2.db'
db = SQLAlchemy(app)


#RoomReserve modules
import RoomReserve.helpers.session
import RoomReserve.homepage
import RoomReserve.helpers.errorhandlers
from RoomReserve.dbtables.user import User
from RoomReserve.dbtables.guest import Guest
from RoomReserve.dbtables.room import Room
from RoomReserve.dbtables.reservation import Reservation
import RoomReserve.admin.user


#this will be helpful for engine reference: http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html

# an Engine, which the Session will use for connection resources
#some_engine = create_engine('postgresql://scott:tiger@localhost/')
#we will need to change the target of the create_engine

# create a configured "Session" class, this is our "session factory" it is recommended that we keep this at the global scope.
#Session = sessionmaker(bind=some_engine)

# the following is an example on how to create a Session, I don't believe we need this at a global scope but can have multiple.
#session = Session()


# Creates database classes as defined in the
# above imports from RoomReserve.dbtables.*
db.create_all()
db.session.commit()

defaultAdmins = []
for me in db.session.query(User).filter_by(email='admin@localhost'):
	defaultAdmins.append(me)
if len(defaultAdmins) > 0:
    #default admin is already created
    print("Default admin account admin@localhost exists.")
else:
    admin = User('Default', 'Admin', 'admin@localhost', 'admin')
    print("Default admin account 'admin@localhost' created. Welcome to RoomReserve.")
    db.session.add(admin)
    db.session.commit()


#admin = User('Dorjee', 'Dhondup', 'dhondo01@luther.edu', 'admin')
#admin2 = User('Ryan', 'Bennett', 'bennry01@luther.edu', 'admin')
#admin3 = User('Zach', 'Stakel', 'dsfd@luther.edu', 'admin')
#print("Default users created.")

#db.session.add(admin)
#db.session.add(admin2)
#db.session.add(admin3)
#db.session.commit()



#users = User.query.all()

import atexit
@atexit.register
def droptables():
    db.drop_all()
    db.session.commit()
    print("All tables are dropped.")
    print("Bye.")



# Try not to add additional page routes in here.

@app.route("/dbtest")
def db_test():
    title = "DB Works!"
    users = User.query.all()
    return render_template('test.html', title=title, users=users)

class test_form(Form):
    name = StringField('name', validators=[DataRequired()])

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
	return render_template('basic.html',title=title)

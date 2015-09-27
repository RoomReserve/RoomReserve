from flask import *
from jinja2 import Template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

@app.route("/")
def page_homepage():
	title="RoomReserve Homepage"
	content = "<strong>Welcome to RoomReserve</strong>"
	return render_template('basic.html', title=title, content=content)


@app.route("/today")
def page_today():
	title="Today's Activity"
	return render_template('basic.html',title=title)





#----Error Pages----
@app.errorhandler(404)
def page_error404(e):
	desc="It looks like the page you were looking for doesn't exist or has been moved.<br />Sorry about that!"
	head="404 - Page Not Found"
	return render_template('error.html',desc=desc,head=head), 404

@app.errorhandler(500)
def page_error500(e):
	desc="Something major has gone wrong. You should check your log files. 500 INTERNAL SERVER ERROR"
	head="500 - Database error"
	return render_template('error.html',desc=desc,head=head), 500




if __name__ == "__main__":
    app.run()

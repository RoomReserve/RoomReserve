from RoomReserve import *

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
		return '<User %r' % (self.email)

	def is_authenticated(self):
		return True

	def is_active(self):
		return not self.role="inactive"

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

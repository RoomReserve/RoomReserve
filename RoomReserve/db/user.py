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
		return '%r %r' % (self.first, self.last)

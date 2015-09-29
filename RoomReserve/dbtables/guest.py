from RoomReserve import *

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

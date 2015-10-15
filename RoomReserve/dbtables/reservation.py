from RoomReserve import *

class Reservation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	guest = db.Column(db.Integer, db.ForeignKey(Guest.id), nullable=False)
	madeby = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	place = db.Column(db.Integer, db.ForeignKey(Room.id), nullable=False)
	checkintime = db.Column(db.DateTime, nullable=False, unique=False)
	checkintime = db.Column(db.DateTime, nullable=False, unique=False)
	status = db.Column(db.String(20), unique=False, nullable=False)
	notes = db.Column(db.String(500), unique=False)

	def __init__(self, guest, madeby, place, time, status="Unarrived", notes=""):
		self.guest = guest
		self.madeby = madeby
		self.place = place
		self.checkintime = checkintime
		self.checkouttime = checkintime
		self.status = status
		self.notes = notes

	def __repr__(self):
		return '%r %r' % (self.time, self.place)

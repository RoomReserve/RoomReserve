from RoomReserve import *

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

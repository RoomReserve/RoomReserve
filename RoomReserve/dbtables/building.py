from RoomReserve import *

class Building(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=False, nullable=False)
	numfloors = db.Column(db.Integer, unique=False, nullable=True)
	description = db.Column(db.String(500), unique=False)
	status = db.Column(db.String(20), unique=False, nullable=False)
	notes = db.Column(db.String(500), unique=False)

	def __init__(self, name, numfloors, status, description="", notes=""):
		self.name = name
		self.numfloors = numfloors
		self.status = status
		self.description = description
		self.notes = notes

	def __repr__(self):
		return '%r %r %r' % (self.roomnumber, self.floor, self.bullding)

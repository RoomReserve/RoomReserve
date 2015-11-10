from RoomReserve import *
from RoomReserve.admin.building import getBuildingById as getBuildingById

class Room(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	roomnumber = db.Column(db.Integer, unique=False, nullable=False)
	buildingID = db.Column(db.Integer, unique=False, nullable=False) #building ID number
	floor = db.Column(db.Integer, unique=False, nullable=True)
	capacity = db.Column(db.Integer, unique=False, nullable=True)
	description = db.Column(db.String(500), unique=False)
	status = db.Column(db.String(20), unique=False, nullable=False)
	notes = db.Column(db.String(500), unique=False)

	def __init__(self, roomnumber, floor, buildingID, capacity, description="", status="Ready", notes=""):
		self.roomnumber = roomnumber
		self.buildingID = buildingID
		self.floor = floor
		self.capacity = capacity
		self.description = description
		self.status = status
		self.notes = notes

	def getMyBuildingName(self):
		return getBuildingById(self.buildingID).getBuildingName()

	def __repr__(self):
		return '%r %r %r' % (self.roomnumber, self.floor, self.bullding)

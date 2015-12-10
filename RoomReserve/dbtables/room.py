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

	def getID(self):
		return self.id
		
	def get_room_number(self):
		# returns the room number of this room
		return self.roomnumber

	def get_building_id(self):
		# returns the buildingID for the building
		# that this room is in
		return self.buildingID

	def get_floor(self):
		# returns the floor number for this room
		return self.floor

	def get_capacity(self):
		# returns the capacity for this room
		return self.capacity

	def get_description(self):
		# returns the description for this room
		return self.description

	def get_status(self):
		# returns the status of the room
		return self.status

	def get_notes(self):
		# returns the notes for this room
		return self.notes

	def set_room_number(self, rn):
		# Changes/sets the room number of the room
		# Returns the new room number. False upon failure
		try:
			self.roomnumber = rn
			db.session.commit()
		except:
			return False
		return self.roomnumber

	def set_building_id(self, bID ):
		# Changes/sets the buildingID of the room
		# Returns the new buildingID. False upon failure
		try:
			self.buildingID = bID
			db.session.commit()
		except:
			return False
		return self.buildingID

	def set_floor(self, fl):
		# Changes/sets the  of the room
		# Returns the new . False upon failure
		try:
			self.floor = fl
			db.session.commit()
		except:
			return False
		return self.floor

	def set_capacity(self, cap):
		# Changes/sets the capacity of the room
		# Returns the new capacity value. False upon failure
		try:
			self.capacity = cap
			db.session.commit()
		except:
			return False
		return self.capacity

	def set_description(self, desc):
		# Changes/sets the description of the room
		# Returns the new description. False upon failure
		try:
			self.description = desc
			db.session.commit()
		except:
			return False
		return self.description

	def set_status(self, st):
		# Changes/sets the status of the room
		# Returns the new status. False upon failure
		# Status codes can be found in RoomReserve.helpers.static_variables
		try:
			self.status = st
			db.session.commit()
		except:
			return False
		return self.status

	def set_notes(self, notes):
		# Changes/sets the notes of the room
		# Returns the new notes value. False upon failure
		try:
			self.notes = notes
			db.session.commit()
		except:
			return False
		return self.notes

	def __repr__(self):
		return '%r %r %r' % (self.roomnumber, self.floor, self.bullding)

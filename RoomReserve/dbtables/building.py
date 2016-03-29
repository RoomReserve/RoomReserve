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
		self.numfloors = int(numfloors)
		self.status = status
		self.description = description
		self.notes = notes

	def getBuildingName(self):
		# See documentation for get_name
		return self.get_name()

	def get_name(self):
		# Returns the name of the building
		return self.name

	def get_floors(self):
		# Returns the number of floors of the building
		return self.numfloors

	def get_description(self):
		# Returns the description of the building
		return self.description

	def get_status(self):
		# Returns the status code of the building
		return self.status

	def get_notes(self):
		# Returns the notes field of the building
		return self.notes

	def set_name(self, name):
		# Changes/sets the name of the building
		# Returns the new name. False upon failure
		try:
			self.name = name
			db.session.commit()
		except:
			return False
		return self.name

	def set_floors(self, fl):
		# Changes/sets the number of floors of the building
		# Returns the number of floors. False upon failure
		try:
			self.numfloors = int(fl)
			db.session.commit()
		except:
			return False
		return self.numfloors

	def set_description(self, desc):
		# Changes/sets the description of the building
		# Returns the new desc. False upon failure
		try:
			self.description = desc
			db.session.commit()
		except:
			return False
		return self.description

	def set_status(self, st):
		# Changes/sets the status of the building
		# Returns the new status. False upon failure
		try:
			self.status = st
			db.session.commit()
		except:
			return False
		return self.status

	def set_notes(self, notes):
		# Changes/sets the note of the building
		# Returns the note. False upon failure
		try:
			self.notes = notes
			db.session.commit()
		except:
			return False
		return self.notes

	def is_deletable(self):
		'''
		A building can be deleted if it has no rooms
		'''
		if len(self.all_rooms()) == 0:
			return True
		return False

	def all_rooms(self):
		'''
		Returns a list of all rooms in the building.
		'''
		from RoomReserve.dbtables.room import Room
		containsRooms = []
		for me in db.session.query(Room).filter(Room.buildingID == self.id):
		    containsRooms.append(me)
		return containsRooms

	def __repr__(self):
		return 'Building %r' % (self.name)

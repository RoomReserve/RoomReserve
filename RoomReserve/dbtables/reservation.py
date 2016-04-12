from RoomReserve import *
from RoomReserve.admin.guest import getGuestByID
from RoomReserve.admin.rooms import getRoomByID

class Reservation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	guestID = db.Column(db.Integer, db.ForeignKey(Guest.id))
	madeby = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	roomID = db.Column(db.Integer, db.ForeignKey(Room.id))
	checkintime = db.Column(db.DateTime, nullable=False, unique=False)
	checkouttime = db.Column(db.DateTime, nullable=False, unique=False)
	status = db.Column(db.String(20), unique=False, nullable=False)
	notes = db.Column(db.String(500), unique=False)

	def __init__(self, guest, madeby, room, checkintime, checkouttime, status=CONST.unarrived_status, notes=""):
		self.madeby = madeby
		self.checkintime = checkintime
		self.checkouttime = checkouttime
		self.status = status
		self.notes = notes

		if status is not CONST.draft_status:
			self.guestID = self.setGuest(guestID=guest)
			self.roomID = self.setRoom(roomID=room)
		else:
			self.guestID = None
			self.roomID = None

	def setRoom(self, roomID=None, room=None):
		class RoomDoesNotExistException(Exception):
			'''
			An exception to throw when a requested room doesn't exist
			'''
			def __init__(self, value):
				self.value = value
			def __str__(self):
				return "Room " + repr(self.value) + " does not exist"

		def roomExists(myid):
			'''
			Checks to see if the roomID corresponds to a valid room
			Returns True if the roomID exists, else False.
			'''
			if getRoomByID(myid):
				return True
			return False

		if room:
			# we were given a room object, get the roomID
			roomID = room.getID()

		if roomExists(roomID):
			self.roomID = roomID
			db.session.commit()
		else:
			raise RoomDoesNotExistException(roomID)

		return self.roomID

	def setGuest(self, guestID=None, guest=None):
		class GuestDoesNotExistException(Exception):
			'''
			An exception to throw when a requested room doesn't exist
			'''
			def __init__(self, value):
				self.value = value
			def __str__(self):
				return "Guest " + repr(self.value) + " does not exist"

		def guestExists(myid):
			'''
			Checks to see if the guestID corresponds to a valid guest
			Returns True if the guestID exists, else False.
			'''
			if getGuestByID(myid):
				return True
			return False

		if guest:
			# we were given a guest object, get the guestID
			guestID=guest.getID()

		if guestExists(guestID):
			self.guestID = guestID
			db.session.commit()
		else:
			raise GuestDoesNotExistException(guestID)

		return self.guestID


	def set_status(self, status):
		self.status = status
		db.session.commit()
		
	def checkin(self):
		if self.status == checkedin_status:
			return True
		else:
			myroom = getRoomByID(self.roomID)
			if myroom.status != ready_status:
				return False
			else:
				self.status = checkedin_status
				db.session.commit()
				myroom.set_status(occupied_status)
				return True
				
	def checkout(self):
		if self.status == checkedout_status:
			return True
		else:
			myroom = getRoomByID(self.roomID)
			self.status = checkedout_status
			db.session.commit()
			myroom.set_status(unclean_status)
			return True

	def getID(self):
		return self.id

	def get_name(self):
		return str(self.getID()) + " (" + self.get_guest().get_name() + ")"

	def roomIsSet(self):
		return self.roomID is not None

	def getRoomID(self):
		return self.roomID

	def get_room(self):
		return getRoomByID(self.getRoomID())

	def guestIsSet(self):
		return self.guestID is not None

	def getGuestID(self):
		return self.guestID

	def get_guest(self):
		return getGuestByID(self.getGuestID())

	def get_check_in_datetime(self):
		return self.checkintime

	def get_check_out_datetime(self):
		return self.checkouttime

	def get_status(self):
		return self.status

	def isDraft(self):
		''' True if reservation is draft status, else false. '''
		return self.get_status() == CONST.draft_status

	def confirm(self):
		'''
		If the reservation has an assigned room and guest,
		the reservation can leave Draft status.
		'''
		if self.isDraft() and self.roomIsSet() and self.guestIsSet():
			self.set_status(CONST.unarrived_status)
			return True
		return False

	def is_deletable(self):
		'''
		A reservation that is checked in (active) cannot be deleted
		'''
		return self.get_status() != CONST.checkedin_status

	def get_delorean(self):
		'''
		Returns the time range for the reservation.
		The range is from the check in date to the check out date,
		does not include the check out date.
		'''
		return delorean_helper.create_delorean(self.checkintime, self.checkouttime)

	def __repr__(self):
		return '<Reservation %r>' % (self.id)

from RoomReserve import *
from RoomReserve.admin.guest import getGuestByID
from RoomReserve.admin.rooms import getRoomByID

class Reservation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	guestID = db.Column(db.Integer, db.ForeignKey(Guest.id), nullable=False)
	madeby = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	roomID = db.Column(db.Integer, db.ForeignKey(Room.id), nullable=False)
	checkintime = db.Column(db.DateTime, nullable=False, unique=False)
	checkouttime = db.Column(db.DateTime, nullable=False, unique=False)
	status = db.Column(db.String(20), unique=False, nullable=False)
	notes = db.Column(db.String(500), unique=False)

	def __init__(self, guest, madeby, room, checkintime, checkouttime, status="Unarrived", notes=""):
		self.guest = self.setGuest(guestID=guest)
		self.madeby = madeby
		self.roomID = self.setRoom(roomID=room)
		self.checkintime = checkintime
		self.checkouttime = checkouttime
		self.status = status
		self.notes = notes

	def setRoom(self, roomID=None, room=None):
		class RoomDoesNotExistException(Exception):
			def __init__(self, value):
				self.value = value
			def __str__(self):
				return "Room " + repr(self.value) + " does not exist"

		def roomExists(myid):
		    if getRoomByID(myid):
		        return True
		    return False

		if room:
			# we were given a room object, get the roomID
			roomID = room.getID()
			if roomExists(roomID):
				self.roomID = roomID
			else:
				raise RoomDoesNotExistException(roomID)
		elif roomID:
			# we were given a roomID, that's exactly what we need
			if roomExists(roomID):
				self.roomID = roomID
			else:
				raise RoomDoesNotExistException(roomID)
		else:
			abort(428, description="Not a valid Room accessor request. \
			You must supply setRoom with a Room object (room=myRoom), \
			or a roomID (roomID=myRoomID).")
		return self.roomID

	def setGuest(self, guestID=None, guest=None):
		class GuestDoesNotExistException(Exception):
			def __init__(self, value):
				self.value = value
			def __str__(self):
				return "Guest " + repr(self.value) + " does not exist"

		def guestExists(myid):
		    if getGuestByID(myid):
		        return True
		    return False

		if guest:
			# we were given a guest object, get the guestID
			guestID=guest.getID()
			if guestExists(guestID):
				self.guestID = guestID
			else:
				raise GuestDoesNotExistException(guestID)

		elif guestID:
			# we were given a guestID, that's exactly what we need
			if guestExists(guestID):
				self.guestID = guestID
			else:
				raise GuestDoesNotExistException(guestID)

		else:
			abort(428, description="Not a valid Guest accessor request. \
			You must supply setGuest with a Guest object (guest=myGuest), \
			or a guestID (guestID=myGuestID).")
		return self.guestID


	def get_delorean(self):
		return delorean_helper.create_delorean(self.checkintime, self.checkouttime)

	def __repr__(self):
		return '<Reservation %r>' % (self.id)

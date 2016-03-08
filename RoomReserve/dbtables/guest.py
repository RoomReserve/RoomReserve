from RoomReserve import *

class Guest(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first = db.Column(db.String(40), unique=False)
	last = db.Column(db.String(40), unique=False)
	email = db.Column(db.String(50), unique=True)
	phone = db.Column(db.String(20), unique=False)
	address = db.Column(db.String(75), unique=False)
	payment = db.Column(db.Integer, unique=False)
	notes = db.Column(db.String(500), unique=False)


	def __init__(self, first, last, email, phone, address, payment=0, notes=""):
		self.first = first
		self.last = last
		self.email = email
		self.phone = phone
		self.address = address
		self.payment = payment
		self.notes = notes

	def get_id(self):
		# Returns the ID of the guest.
		return self.id

	def getID(self):
		# Alias for self.get_id()
		return self.get_id()

	def get_first_name(self):
		# Returns the first name of the guest
		return self.first

	def get_last_name(self):
		# Returns the last name of the guest
		return self.last

	def get_email(self):
		# Returns the email of the guest
		return self.email

	def get_address(self):
		# Returns the address of the guest
		return self.address

	def get_payment(self):
		# Returns the payment amount of the guest
		return self.payment

	def get_notes(self):
		# Returns the notes of the guest
		return self.notes

	def set_first_name(self, fn):
		# Changes/sets the first name of the guest
		# Returns the new name. False upon failure
		try:
			self.first = fn
			db.session.commit()
		except:
			return False
		return self.first

	def set_last_name(self, ln):
		# Changes/sets the last name of the guest
		# Returns the new name. False upon failure
		try:
			self.last = fn
			db.session.commit()
		except:
			return False
		return self.last

	def set_email(self, em):
		# Changes/sets the email of the guest
		# Returns the new email. False upon failure
		try:
			self.email = em
			db.session.commit()
		except:
			return False
		return self.email

	def set_phone(self, ph):
		# Changes/sets the phone number of the guest
		# Returns the phone number. False upon failure
		try:
			self.phone = ph
			db.session.commit()
		except:
			return False
		return self.phone

	def set_address(self, addr):
		# Changes/sets the address of the guest
		# Returns the new address. False upon failure
		try:
			self.address = addr
			db.session.commit()
		except:
			return False
		return self.address

	def set_payment(self, pmt):
		# Changes/sets the payment amount of the guest
		# Returns the new payment amount. False upon failure
		try:
			self.payment = pmt
			db.session.commit()
		except:
			return False
		return self.payment

	def set_notes(self, notes):
		# Changes/sets the notes field of the guest
		# Returns the new notes value. False upon failure
		try:
			self.notes = notes
			db.session.commit()
		except:
			return False
		return self.notes

	def __repr__(self):
		return '%r %r' % (self.first, self.last)

from RoomReserve import *
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first = db.Column(db.String(40), unique=False)
	last = db.Column(db.String(40), unique=False)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(160), unique=False)
	role = db.Column(db.String(100), unique=False)
	#	Possible roles:
	#	- admin
	#	- standard
	#	- readonly
	#	- inactive


	def __init__(self, first, last, email, role, password):
		self.first = first
		self.last = last
		self.email = email
		self.role = role
		self.password = self.generate_password(password)

	def __repr__(self):
		return '<User %r>' % (self.email)

	def generate_password(self, pw_plaintext):
		# Returns a SHA-1 salted password from the given plaintext password
		return generate_password_hash(pw_plaintext)

	def check_password(self, pw_plaintext):
		# Checks to see if the plaintext password matches the SHA-1 password
		# that's in the database.
		# Returns True/False
		return check_password_hash(self.password, pw_plaintext)

	def is_authenticated(self):
		# Are we logged in?
		# returns True/False
		return True

	def is_admin(self):
		# Is this user an admin?
		# returns True/False
		return self.role=="admin"

	def is_standard(self):
		# Is this user a standard user or above?
		# returns True/False
		return self.role=="standard" or is_admin(self)

	def is_readonly(self):
		# Is this user a readonly user or above?
		# returns True/False
		return self.role=="readonly" or is_standard(self)

	def getName(self):
		# Return this users full name in a string.
		return self.first + " " + self.last

	def getEmail(self):
		# Return this users email address
		return self.email

	def getRole(self):
		# Return this users role
		return self.role

	def is_active(self):
		# Returns True/False if this user is not inactive
		return not self.role=="inactive"

	def is_inactive(self):
		# Returns True/False if this user is inactive
		return not self.is_active()

	def is_anonymous(self):
		# This user is not anonymous (thus, is logged in)
		return False

	def get_id(self):
		# return this user's id # from the database
		return self.id

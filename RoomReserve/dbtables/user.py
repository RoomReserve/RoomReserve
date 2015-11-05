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
		return generate_password_hash(pw_plaintext)

	def check_password(self, pw_plaintext):
		return check_password_hash(self.password, pw_plaintext)

	def is_authenticated(self):
		return True

	def is_admin(self):
		return self.role=="admin"

	def is_standard(self):
		return self.role=="standard"

	def is_readonly(self):
		return self.role=="readonly"

	def getName(self):
		return self.first + " " + self.last

	def getEmail(self):
		return self.email
		
	def getRole(self):
		return self.role

	def is_active(self):
		return not self.role=="inactive"

	def is_inactive(self):
		return not self.is_active()

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

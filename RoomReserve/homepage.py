from RoomReserve import *

@app.route("/")
@app.route("/index")
def page_homepage():

	title="RoomReserve"
	content = "<strong>Welcome to RoomReserve!</strong> =)"

	# if 'username' in session:
	#     content += ' Logged in as %s' % escape(session['username'])

	return render_template('basic.html', title=title, content=content)

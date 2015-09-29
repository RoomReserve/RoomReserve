from RoomReserve import *

@app.route("/")
def page_homepage():

	title="RoomReserve Homepage"
	content = "<strong>Welcome to RoomReserve.</strong>"

	if 'username' in session:
	    content += ' Logged in as %s' % escape(session['username'])

	return render_template('basic.html', title=title, content=content, session=session)

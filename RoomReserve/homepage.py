from RoomReserve import *

@app.route("/")
def page_homepage():
	title="RoomReserve Homepage"
	content = "<strong>Welcome to RoomReserve</strong>"
	return render_template('basic.html', title=title, content=content)

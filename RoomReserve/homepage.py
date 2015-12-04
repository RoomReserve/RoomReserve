from RoomReserve import *

@app.route("/")
@app.route("/index")
@login_required
def index():

	title="RoomReserve"
	content = "<strong>Welcome to RoomReserve!</strong>"
	# content += "\n debug: running on " + sys.platform


	return render('basic.html', title=title, content=content)

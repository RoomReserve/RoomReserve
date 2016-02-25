from RoomReserve import *

@app.route("/")
@app.route("/index")
@login_required
def index():

	title="RoomReserve"
	content = ""



	return render('homepage.html', title=title, content=content)

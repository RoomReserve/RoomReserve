from RoomReserve import *

@app.route("/admin/dashboard")
@login_required
def dashboard():

	title="Dashboard"
	content = ""


	return render('dashboard.html', title=title, content=content)
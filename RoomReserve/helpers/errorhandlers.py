from RoomReserve import *

#----Error Pages----
@app.errorhandler(404)
def page_error404(e):
	desc="It looks like the page you were looking for doesn't exist or has been moved.<br />Sorry about that!"
	title="404 - Page Not Found"
	return render('error.html',desc=desc,title=title), 404

@app.errorhandler(500)
def page_error500(e):
	desc="Something major has gone wrong. You should check your log files. 500 INTERNAL SERVER ERROR"
	desc += "\n"
	try:
		desc += str(e)
	except:
		desc += "Error not displayed."
	title="500 - Database error"
	return render('error.html',desc=desc,title=title), 500

@app.errorhandler(400)
def page_error400(e):
	desc="Your browser made a request that this application couldn't understand."
	title="400 - Bad Request"
	return render('error.html',desc=desc,title=title), 400

@app.errorhandler(405)
def page_error400(e):
	desc="The method you used is not allowed. Check your @app.route('/pageurl', methods=['methodTypes'])."
	desc+=" -- You probably forgot to add methods=['GET','POST']"
	title="405 - Method not allowed"
	return render('error.html',desc=desc,title=title), 405

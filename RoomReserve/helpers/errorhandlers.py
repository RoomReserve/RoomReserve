from RoomReserve import *
import traceback


#----Error Pages----
@app.errorhandler(404)
def page_error404(e):
	desc="It looks like the page you were looking for doesn't exist or has been moved.<br />Sorry about that!"
	title="404 - Page Not Found"
	return render('error.html',desc=desc,title=title), 404

@app.errorhandler(500)
def page_error500(e):
	desc="There is a coding error. The stack trace is printed below."
	desc += "\n"
	try:
		desc += '\n' + str(traceback.format_exc())
	except:
		desc += "\n Error not displayed."
	title="500 - Internal Server Error"
	desc = desc.replace('\n', '<br>')
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

@app.errorhandler(501)
def page_error501(e):
	desc="An error occurred. The opetation may not have completed."
	title="Database Error"
	return render('error.html',desc=desc,title=title), 501

from flask import *
from jinja2 import Template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://tmp/temp.db'
db = SQLAlchemy(app)



@app.route("/")
def page_homepage():
	title="RoomReserve Homepage"
	content = "<strong>Welcome to RoomReserve</strong>"
	return render_template('basic.html', title=title, content=content)


@app.route("/today")
def page_today():
	title="Today's Activity"
	return render_template('basic.html',title=title)




@app.route("/hello")
def page_hello():
    # return "Hello World!"
    title = "Test Works"
    p = "Hello World!"
    return render_template('test.html', title=title,p=p)




#----Error Pages----
@app.errorhandler(404)
def page_error404(e):
	desc="It looks like the page you were looking for doesn't exist or has been moved.<br />Sorry about that!"
	head="404 - Page Not Found"
	return render_template('error.html',desc=desc,head=head), 404

@app.errorhandler(500)
def page_error500(e):
	desc="Something major has gone wrong. You should check your log files. 500 INTERNAL SERVER ERROR"
	head="500 - Database error"
	return render_template('error.html',desc=desc,head=head), 500


if __name__ == "__main__":
    app.run()
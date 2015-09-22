from flask import *
from jinja2 import Template
app = Flask(__name__)


@app.route("/")
def hello():
    # return "Hello World!"
    title = "Hello Template"
    p = "Hello World! This is a test page!"
    return render_template('test.html', title=title,p=p)

if __name__ == "__main__":
    app.run()
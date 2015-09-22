from flask import *
from jinja2 import Template
app = Flask(__name__)


@app.route("/")
def hello():
    # return "Hello World!"
    title = "Test Works"
    p = "Hello World!"
    return render_template('test.html', title=title,p=p)

if __name__ == "__main__":
    app.run()
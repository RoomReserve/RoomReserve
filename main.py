from flask import *
from jinja2 import Template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://tmp/temp.db'
db = SQLAlchemy(app)



@app.route("/")
def hello():
    # return "Hello World!"
    title = "Test Works"
    p = "Hello World!"
    return render_template('test.html', title=title,p=p)

if __name__ == "__main__":
    app.run()

print('Hello!')
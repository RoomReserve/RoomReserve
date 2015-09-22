from flask import *
app = Flask(__name__)

app.run(debug=True) 
'''enable debugging '''


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()

from flask import Flask

# make the application
app = Flask(__name__)

# make the route
@app.route("/")

#def a function
def hello:
    return "Hello World!!"


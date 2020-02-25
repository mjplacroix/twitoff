
from flask import Flask, render_template

# make the application
app = Flask(__name__)

# make the route
@app.route("/")

#def a function
def hello():
    return "Hello World!!"

# make second route
@app.route("/about")

# func for about
def preds():
    return render_template('about.html')


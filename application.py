import os
import re
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue

from cs50 import SQL

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///dorm.db")

@app.route("/")
def index():
    """Render map."""
    
    # check if API key is set
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))

@app.route("/update")
def update():
    """Update floor plan images."""
    
    # ensure parameters are present
    if not request.args.get("floor"):
        raise RuntimeError("missing floor")
    
    # query database for images of current floor
    rows = db.execute("SELECT * FROM images JOIN imbounds ON images.house = imbounds.house WHERE floor = :floor", 
                        floor=request.args.get("floor"))
    
    # output images as JSON
    return jsonify([rows])
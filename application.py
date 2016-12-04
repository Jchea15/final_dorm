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
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))

@app.route("/get_images")
def get_images():
    """Get floor plan images."""
    # ensure parameters are present
    if not request.args.get("floor"):
        raise RuntimeError("missing floor")
    # query database for images of current floor
    rows = db.execute("SELECT * FROM images JOIN imbounds ON images.house = imbounds.house WHERE floor = :floor", 
                        floor=request.args.get("floor"))
    return jsonify([rows])

# temporarily disable so can try drop-downs
# @app.route("/search")
# def search():
#     if not request.args.get("room"):
#        return failure.html
#     if request.args.get("floor"):
#         return failure.html
#     if request.args.get("dorm"):
#         return failure.html
#     selection= db.execute("SELECT * FROM rooms WHERE room=:room AND floor=:floor AND dorm=:dorm", room=request.args.get("room"), floor=request.args.get("floor"), dorm=request.args.get("dorm"))
#     return jsonify(selection)
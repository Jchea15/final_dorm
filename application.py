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
    floor=request.args.get("floor")
    # query database for images of current floor
    rows = db.execute("SELECT * FROM images JOIN imbounds ON images.house = imbounds.house WHERE floor = :floor", 
                        floor=floor)
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

# marianne -> but if you drag you want to be able to see rooms, I think we should have this set up
# @app.route("/update")
# def update():
#     """Find up to 10 places within view."""

#     # ensure parameters are present
#     if not request.args.get("sw"):
#         raise RuntimeError("missing sw")
#     if not request.args.get("ne"):
#         raise RuntimeError("missing ne")

#     # ensure parameters are in lat,lng format
#     if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
#         raise RuntimeError("invalid sw")
#     if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
#         raise RuntimeError("invalid ne")

#     # explode southwest corner into two variables
#     (sw_lat, sw_lng) = [float(s) for s in request.args.get("sw").split(",")]

#     # explode northeast corner into two variables
#     (ne_lat, ne_lng) = [float(s) for s in request.args.get("ne").split(",")]

#     # find 10 cities within view, pseudorandomly chosen if more within view
#     if (sw_lng <= ne_lng):

#         # doesn't cross the antimeridian
#         rows = db.execute("""SELECT * FROM rooms
#             WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
#             GROUP BY room, floor, dorm
#             ORDER BY RANDOM()
#             LIMIT 10""",
#             sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

#     else:

#         # crosses the antimeridian
#         rows = db.execute("""SELECT * FROM rooms
#             WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
#             GROUP BY room, floor, dorm
#             ORDER BY RANDOM()
#             LIMIT 10""",
#             sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

#     # output places as JSON
#     return jsonify(rows)
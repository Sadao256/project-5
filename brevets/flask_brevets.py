"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging
from pymongo import MongoClient

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

# Set up MongoDB connection
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27018)

# Select or create the database
db = client['brevet_database']

# Define a collection (similar to a table in relational databases)
brevet_collection = db['brevet_collection']

###
# Pages
###

def display_data():
    """
    Obtains the newest document in the "lists" collection in database "todo".

    Returns title (string) and items (list of dictionaries) as a tuple.
    """
    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.
    form_data = brevet_collection.find().sort("_id", -1).limit(1)

    # lists is a PyMongo cursor, which acts like a pointer.
    # We need to iterate through it, even if we know it has only one entry:
    for data in form_data:
        return data["distance"], data["begin_date"], data["controls"]


def submit_data(distance, begin_date, controls):
    """
    Returns the unique ID assigned to the document by mongo (primary key.)
    """
    output = brevet_collection.insert_one({
                     "distance": distance,
                     "begin_date": begin_date,
                     "controls": controls
                  })
    _id = output.inserted_id # this is how you obtain the primary key (_id) mongo assigns to your inserted document.
    return str(_id)



@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404

@app.route("/submit_btn", methods=["POST"])
def submit():
    try: 
        input_json = request.json
        distance = input_json["distance"] 
        begin_date = input_json["begin_date"] 
        controls = input_json["controls"]

        data_id = submit_data(distance, begin_date, controls)

        return flask.jsonify(result={},
            message="Inserted!", 
            status=1, # This is defined by you. You just read this value in your javascript.
            mongo_id=data_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')

@app.route("/display_btn")
def display():
        try:
            distance, begin_date, controls = display_data()
            return flask.jsonify(
                result={"distance": distance, "begin_date": begin_date, "controls":controls}, 
                status=1,
                message="Successfully fetched a to-do list!")
        except:
            return flask.jsonify(
                result={}, 
                status=0,
                message="Something went wrong, couldn't fetch any lists!")

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from kilometers, using rules
    described at https://rusa.org/octime_alg.html.
    Expects three URL-encoded arguments: km, start_time, and brevet_dist.
    """
    app.logger.debug("Got a JSON request")
    
    # Get the Km from the Ajax request
    km = request.args.get('km', 999, type=float)
    
    # Get the start time from the Ajax request
    start_time_str = request.args.get('start_time')

    # Get the Brevet Distance from the Ajax request
    brevet_dist = request.args.get('brevet_dist', 200, type=int)
    
    # Convert the start_time string to an arrow object
    start_time = arrow.get(start_time_str)

    # calculate the open time with the arguements km, brevet_dist, start_time using open_time function in the file acp_times
    open_time = acp_times.open_time(km, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')

    # calculate the close time with the arguements km, brevet_dist, start_time using close_time function in the file acp_times
    close_time = acp_times.close_time(km, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')

    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")

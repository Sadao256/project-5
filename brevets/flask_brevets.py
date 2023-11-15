"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
from mongo_db import fetch_data, insert_data

import logging



###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404

@app.route("/insert", methods=["POST"])
def insert():
    try: 
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!
        
        # Because input_json is a dictionary, we can do this:
        brevet = input_json["brevet"] 
        begin_date = input_json["begin_date"] 
        controls = input_json["controls"]

        todo_id = insert_data(brevet, begin_date, controls)

        return flask.jsonify(result={},
            message="Inserted!", 
            status=1, # This is defined by you. You just read this value in your javascript.
            mongo_id=todo_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')

@app.route("/fetch")
def fetch():
        """
        /fetch : fetches the newest to-do list from the database.

        Accepts GET requests ONLY!

        JSON interface: gets JSON, responds with JSON
        """
        try:
            brevet, begin_date, controls = fetch_data()
            return flask.jsonify(
                result={"brevet": brevet, "begin_date": begin_date, "controls":controls}, 
                status=1,
                message="Successfully fetched a brevet list!")
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

"""
Nose tests for flask_brevets.py
Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
import logging

from flask_brevets import fetch_data, insert_data # import function fetch_data and insert_data from flask_brevets

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_fetch():
    # a response object with JSON data.
    response = fetch_data()

    data = response.get_json()  # JSON data
    assert "result" in data  # Check if the response contains the "result" key
    assert "brevet" in data["result"]  # Check if the "result" contains "brevet" key
    assert "begin_date" in data["result"]  # Check if the "result" contains "begin_date" key
    assert "controls" in data["result"]  # Check if the "result" contains "controls" key

def test_insert():
    # test input JSON for brevet, begin_date, and controls
    test_input = {
        "brevet": "test_brevet",
        "begin_date": "2023-01-01T00:00",  # Assuming a valid date format
        "controls": [{"km": 100, "open": "2023-01-01T01:00", "close": "2023-01-01T05:00"}]
    }

    # response object with JSON data.
    response = insert_data(test_input)

    data = response.get_json()  # JSON data
    assert "result" in data  # Check if the response contains the "result" key
    assert "message" in data  # Check if the response contains the "message" key
    assert "status" in data  # Check if the response contains the "status" key
    assert "mongo_id" in data  # Check if the response contains the "mongo_id" key

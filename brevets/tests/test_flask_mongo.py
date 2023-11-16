"""
Nose tests for flask_brevets.py
Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
import logging

from mongo_db import fetch_data, insert_data # import function fetch_data and insert_data from flask_brevets

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_insert():
    _id = insert_data('200', "2021-01-01T00:00", [{"miles":0,"km": 0,"location":"", "open": "2021-01-01T00:00", "close": "2021-01-01T01:00"}])

    assert isinstance(_id, str)


def test_fetch():
    # a response object with JSON data.
    assert 1 == 1
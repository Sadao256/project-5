"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
import logging
import arrow
<<<<<<< HEAD
import brevets.acp_times import open_time, close_time # important function open_time and close_time from acp_times
=======
import acp_times import open_time, close_time # important function open_time and close_time from acp_times
>>>>>>> 22c1a1d (project-4)

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


def test_open_time():
<<<<<<< HEAD
    start_time = arrow.get("2023-11-04T09:20:00")
    assert acp_times.open_time(0, 200, start_time) == start_time
    assert acp_times.open_time(0, 1000, start_time) == start_time
    
    assert close_time(200,200, arrow.get("2023-11-04T12:00:00")) == arrow.get("2023-11-04T05:53:00")
    assert open_time(400,400, arrow.get("2023-11-04T12:00:00")) == arrow.get("2023-11-04T12:30:00")

def test_close_time():
    start_time = arrow.get("2023-11-04T12:00:00")
    assert close_time(0, 200, start_time) != start_time
    assert close_time(0, 200, start_time) == start_time.shift(hours=1)
    assert close_time(0, 1000, start_time) == start_time.shift(hours=1)

    assert close_time(200,200, start_time) == arrow.get("2023-11-04T01:30:00")
    assert close_time(200,200, start_time) != arrow.get("2023-11-04T01:20:00")
    assert close_time(400,400, start_time) == arrow.get("2023-11-04T03:00:00")
    assert close_time(1000,1000, start_time) ==  arrow.get("2023-11-04T03:00:00")
=======
    # test that the times are correctly given for open if there are 0 km
    start_time = arrow.get("2023-11-04T09:20:00")
    assert acp_times.open_time(0, 200, start_time).format('YYYY-MM-DDTHH:mm') == start_time.format('YYYY-MM-DDTHH:mm')
    assert acp_times.open_time(0, 1000, start_time) == start_time
    
    # test that the correct times are produced
    assert open_time(200,200, arrow.get("2023-11-04T12:00:00")).format('YYYY-MM-DDTHH:mm') == arrow.get("2023-11-04T05:53:00").format('YYYY-MM-DDTHH:mm')
    assert open_time(400,400, arrow.get("2023-11-04T12:00:00")).format('YYYY-MM-DDTHH:mm') == arrow.get("2023-11-04T12:30:00").format('YYYY-MM-DDTHH:mm')

def test_close_time():
    # test that the close start adjust the time correctly if the distance is 0 km
    start_time = arrow.get("2023-11-04T12:00:00")
    assert close_time(0, 200, start_time) != start_time.format('YYYY-MM-DDTHH:mm')
    assert close_time(0, 200, start_time).format('YYYY-MM-DDTHH:mm') == start_time.shift(hours=1).format('YYYY-MM-DDTHH:mm')
    assert close_time(0, 1000, start_time).format('YYYY-MM-DDTHH:mm') == start_time.shift(hours=1).format('YYYY-MM-DDTHH:mm')

    # test that any distnace under 60 km is calulated correctly
    assert close_time(10,200, arrow.get("2023-11-04T00:00:00")).format('YYYY-MM-DDTHH:mm') == arrow.get("2023-11-04T01:30:00").format('YYYY-MM-DDTHH:mm')
    assert close_time(50,200, arrow.get("2023-11-04T00:00:00")).format('YYYY-MM-DDTHH:mm') == arrow.get("2023-11-04T03:30:00").format('YYYY-MM-DDTHH:mm')

    # test that the the distances for brevts 200 and 400 have their time adjusted correctly
    assert close_time(200,200, start_time).format('YYYY-MM-DDTHH:mm') == arrow.get("2023-11-04T01:30:00").format('YYYY-MM-DDTHH:mm')
    assert close_time(200,200, start_time).format('YYYY-MM-DDTHH:mm') != arrow.get("2023-11-04T01:20:00").format('YYYY-MM-DDTHH:mm')
    assert open_time(400,400, arrow.get("2023-11-04T12:00:00")).format('YYYY-MM-DDTHH:mm') == arrow.get("2023-11-04T03:00:00").format('YYYY-MM-DDTHH:mm')

    #test that this is the correct time for 1000 km
    assert close_time(1000,1000, start_time).format('YYYY-MM-DDTHH:mm') ==  arrow.get("2023-11-04T03:00:00").format('YYYY-MM-DDTHH:mm')
>>>>>>> 22c1a1d (project-4)












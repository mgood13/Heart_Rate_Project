import pytest
import json


@pytest.mark.parametrize("i, timecheck, voltagecheck, qualitylist", [
    ('test1Process.csv', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
     [0, 0.5, 1, 0.5, 0.25, 0.7, 1.5, 2, 0.5, 0.2],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),

    ])
def test_fileparser(i, timecheck, voltagecheck, qualitylist):
    """Tests to ensure the parser extracts data properly

    This method uses some dummy data in the file test1Process.csv to
    determine whether the fileparser is working.

    :param i: The filename
    :param timecheck: List of correct time values
    :param voltagecheck: List of correct voltage values
    :param qualitylist: Quality list for calling the parser
    :returns time: List containing the time values
    :returns voltage: List containing the voltage values
    """
    from Processing import fileparser

    time, voltage = fileparser(i, qualitylist)
    assert time == timecheck
    assert voltage == voltagecheck
    return time, voltage


@pytest.mark.parametrize("time, voltage, calccheck", [
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
     [0, 0.5, 1, 0.5, 0.25, 0.7, 1.5, 2, 0.5, 0.2], [0, 2, 9, 10]),
    ([3, 6, 12, 13, 18], [8, 4, -5, 3, 10], [-5, 10, 15, 5])

    ])
def test_ecgmathcalc(time, voltage, calccheck):
    """Method that checks the function of the simple math method

    This method uses dummy data presented above and also the data from
    the first test to check the simple math.

    :param time: List of the time values
    :param voltage: List of the voltage values
    :param calccheck: List of correct values to check the calculations
    """
    qualitylist = []
    from Processing import ecgmathcalc
    from Processing import fileparser
    results = ecgmathcalc(time, voltage)

    assert results[0] == calccheck[0]
    assert results[1] == calccheck[1]
    assert results[2] == calccheck[2]
    assert results[3] == calccheck[3]

    i = 'test_data1.csv'
    timelen = len(time)
    for x in range(0, 10000):
        qualitylist.append(1)
    time, voltage = fileparser(i, qualitylist)
    results = ecgmathcalc(time, voltage)
    assert results[0] == -0.68
    assert results[1] == 1.05
    assert results[2] == 27.775
    assert results[3] == 10000


def test_differentiator():
    """This method tests the function of the derivative method

    This method uses a short segment of one of the test files to assess
    the function of the derivative method. It generates the qualitylist
    in the middle of the function with all 1's because this section
    of the data contains all real numbers.

    :returns time: List of the time values
    :returns voltage: List of the voltage values
    :returns timelen: Length of the time list
    :returns diff_vec: Vector of the derivative values
    """
    from Processing import fileparser
    from Processing import differentiator
    from pytest import approx
    qualitylist = []
    test = [0, 0, 0, 0, 0, 0, 0, 8.333333333, -5, -3.333333333,
            -1.666666667, -5, 1.666666667, -1.666666667, -5,
            -2.5, -1.666666667, 5, 5, -6.666666667, -2.5,
            -3.333333333, 3.333333333, 8.333333333, 10,
            -6.666666667, -11.66666667, -5, -10, 5, -6.666666667,
            -1.666666667, -3.333333333, -7.5, 0, 0, 3.333333333,
            3.333333333, -5, -3.333333333, -5, 0, 0, 0,
            1.666666667, -3.333333333, -3.333333333, 10,
            3.333333333, 0, -1.666666667, -2.5, -6.666666667,
            5, -3.333333333, 6.666666667, -5, -3.333333333,
            -5, -1.666666667, -7.5, -8.333333333, -8.333333333,
            0, -6.666666667, -25, -10, 0, 20, 47.5, 36.66666667,
            50, 63.33333333, 85, 122.5, 53.33333333, 20, -25,
            -122.5, -116.6666667, -111.6666667, -66.66666667,
            -23.33333333, 5, 18.33333333, 13.33333333,
            1.666666667, -5, -3.333333333, 5, 1.666666667,
            3.333333333, 2.5, -3.333333333, -5, -1.666666667,
            7.5, -6.666666667, 3.333333333]
    i = 'test_data1_short.csv'
    for x in range(0, 100):
        qualitylist.append(1)
    time, voltage = fileparser(i, qualitylist)
    timelen = len(time)
    diff_vec = differentiator(timelen, voltage, time)
    assert diff_vec == approx(test)
    return time, voltage, timelen, diff_vec


def test_beatcounter():
    """Test for the beat counter

    This method tests the beat counter using the data that was generated
    from the short segment of test data in the previous test.

    :returns beatcount: Number of beats detected
    :returns beat_time: Time of all of the beats
    :returns time: List of time values
    :returns timelen: Length of the time list
    """
    test_time = [0.2]
    from Processing import beatcounter
    time, voltage, timelen, diff_vec = test_differentiator()
    beatcount, beat_time = beatcounter(timelen, diff_vec, time)
    assert beatcount == 1
    assert beat_time == test_time
    return beatcount, beat_time, time, timelen


def test_heartratecalc():
    """Test for the average heart rate calculator

    This method applies the heart rate calculator to the data from the
    above test and then also from a very short example data set of beats.

    """
    from Processing import heartratecalc
    from pytest import approx
    beatcount, beat_time, time, timelen = test_beatcounter()
    duration = time[timelen-1] - time[0]
    assert heartratecalc(beatcount, beat_time, duration, 1) == \
        approx(218.1818)

    beatcount = 5
    beat_time = [3.4, 5.8, 15.7, 30, 65]
    duration = 70
    # The first beats are more rapid -> shorten the window, higher HR
    assert heartratecalc(beatcount, beat_time, duration, 1) == 4
    assert heartratecalc(beatcount, beat_time, duration, 0.5) == 6


def test_jsonout():
    """Tests the validity of the json output

    This method determines whether the output that is created is in true
    json format.

    """
    from Processing import jsonout
    from Processing import fileprocessor
    i, metrics = fileprocessor()
    outputstr = jsonout(i, metrics)
    assert json.loads(outputstr)

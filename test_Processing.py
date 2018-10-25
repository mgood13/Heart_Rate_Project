import pytest

@pytest.mark.parametrize("i, timecheck, voltagecheck", [
    ('test1Process.csv', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 0.5, 1, 0.5, 0.25, 0.7, 1.5, 2, 0.5, 0.2]),

    ])
def test_fileparser(i, timecheck, voltagecheck):
    from Processing import fileparser

    time, voltage = fileparser(i)
    assert time == timecheck
    assert voltage == voltagecheck
    return time, voltage


@pytest.mark.parametrize("time, voltage, calccheck", [
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 0.5, 1, 0.5, 0.25, 0.7, 1.5, 2, 0.5, 0.2], [0, 2, 9, 10]),
    ([3, 6, 12, 13, 18], [8, 4, -5, 3, 10], [-5, 10, 15, 5])

    ])
def test_ecgmathcalc(time, voltage, calccheck):
    from Processing import ecgmathcalc
    from Processing import fileparser
    results = ecgmathcalc(time, voltage)

    assert results[0] == calccheck[0]
    assert results[1] == calccheck[1]
    assert results[2] == calccheck[2]
    assert results[3] == calccheck[3]

    i = 'test_data1.csv'
    time, voltage = fileparser(i)
    results = ecgmathcalc(time, voltage)
    assert results[0] == -0.68
    assert results[1] == 1.05
    assert results[2] == 27.775
    assert results[3] == 10000


def test_differentiator():
    from Processing import fileparser
    from Processing import differentiator
    from pytest import approx
    test = [0,0,0,0,0,0,0,8.333333333,-5,-3.333333333,-1.666666667,-5,1.666666667,-1.666666667,-5,-2.5,-1.666666667,5,5,-6.666666667,-2.5,-3.333333333,3.333333333,8.333333333,10,-6.666666667,-11.66666667,-5,-10,5,-6.666666667,-1.666666667,-3.333333333,-7.5,0,0,3.333333333,3.333333333,-5,-3.333333333,-5,0,0,0,1.666666667,-3.333333333,-3.333333333,10,3.333333333,0,-1.666666667,-2.5,-6.666666667,5,-3.333333333,6.666666667,-5,-3.333333333,-5,-1.666666667,-7.5,-8.333333333,-8.333333333,0,-6.666666667,-25,-10,0,20,47.5,36.66666667,50,63.33333333,85,122.5,53.33333333,20,-25,-122.5,-116.6666667,-111.6666667,-66.66666667,-23.33333333,5,18.33333333,13.33333333,1.666666667,-5,-3.333333333,5,1.666666667,3.333333333,2.5,-3.333333333,-5,-1.666666667,7.5,-6.666666667,3.333333333]
    i = 'test_data1_short.csv'
    time, voltage = fileparser(i)
    timelen = len(time)
    diff_vec = differentiator(timelen, voltage, time)
    assert diff_vec == approx(test)

#def test_beatcounter():



#def test_heartratecalc():

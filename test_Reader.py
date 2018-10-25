def test_csvfinder():
    """Tests the csvfinder function

    :return:
    """
    from Reader import csvfinder
    test_files = csvfinder('./unit_test_data')

    assert test_files.count('poorform') == 0
    assert test_files.count('wrongend') == 0
    assert test_files.count('false.csv') == 1
    assert test_files.count('mess.csv') == 1
    assert test_files.count('poorform.csv') == 1
    assert test_files.count('tab.csv') == 1
    assert test_files.count('test_data1.csv') == 1
    assert test_files.count('words.csv') == 1


def test_csvchecker():
    from Reader import csvchecker




def test_floatcheck():
    from Reader import floatcheck





def test_csvfinder():
    """Tests the csvfinder function

    :return:
    """
    from Reader import csvfinder
    test_files = csvfinder()

    assert test_files.count('poorform') == 0
    assert test_files.count('wrongend') == 0
    assert test_files.count('false.csv') == 1
    assert test_files.count('mess.csv') == 1
    assert test_files.count('poorform.csv') == 1
    assert test_files.count('tab.csv') == 1
    assert test_files.count('test_data1.csv') == 1
    assert test_files.count('words.csv') == 1
    assert test_files.count('test1.csv') == 1
    assert test_files.count('test2.csv') == 1
    return test_files


def test_csvchecker():
    from Reader import csvchecker
    test_files = test_csvfinder()
    check_files = csvchecker(test_files)
    assert 'false.csv' not in check_files
    assert 'mess.csv' not in check_files
    assert 'poorform.csv' not in check_files
    assert 'tab.csv' not in check_files
    assert 'false.csv' not in check_files
    assert 'test2.csv' not in check_files


def test_floatcheck():
    from Reader import floatcheck





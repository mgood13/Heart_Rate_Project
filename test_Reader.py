def test_csvFinder():
    from Reader import csvFinder
    test_files = csvFinder('./unit_test_data')

    assert test_files.count('test2') == 0
    assert test_files.count('test2.csv') == 1










#def test_csvChecker():








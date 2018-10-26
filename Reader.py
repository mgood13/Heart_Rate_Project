import csv
import os


def filereader():
    """The main file reader function.

    :return finaldictionary: The dictionary containing the file names
    and their dialect for the csv reader
    """
    outdictionary = {}
    finaldictionary = {}

    files = csvfinder()

    outdictionary = csvchecker(files)
    finaldictionary = floatcheck(outdictionary)
    return finaldictionary


def csvfinder(direc='.'):
    """Method that finds all .csv files in a given directory.

    :param direc: The desired directory to find files in.
    :return files: The list of .csv files.
    """
    # This method finds all files that end in .csv
    files = [f for f in os.listdir(direc) if f.endswith(".csv")]
    return files


def csvchecker(files):
    """Method that checks every file for being a true .csv with no other delimiters

    :param files: The list of .csv files in the directory
    :return:
    """
    # This method checks all .csv files to see if they are valid csv files
    outdictionary = {}
    count = 0
    for f in files:
        with open(f, 'r') as csv1:
            errornum = 0
            # Attempt to determine the delimiter type
            try:
                dialect = csv.Sniffer().sniff(csv1.read(), delimiters=',')
            except csv.Error:
                errornum = 1

            if errornum == 0:
                outdictionary[f] = dialect
                count += 1
    outdictionary['FileNumber'] = count
    # Return dictionary with file names, qualitylist, and number of valid files
    return outdictionary


def floatcheck(indictionary):
    """Method that checks if every element in the csv can be converted to a number
    and marks the rows with errors

    :param indictionary: Dictionary that contains all real .csv file names
     and a list describing the validity of each row
    :return indictionary: Dictionary containing all .csv files as keys.
    The values are a list indicating good (1) and bad (0) rows.
    """

    temp = 0
    val = 0
    badlist = []

    for f in indictionary:
        qualitylist = []
        count = 1
        errornum = 0
        if f == 'FileNumber':
            continue
        else:
            with open(f, 'r') as csv2:

                dialect = indictionary.get(f)
                reader = csv.reader(csv2, dialect)

                # Populates the lists for time and voltage
                for row in reader:
                    try:
                        temp = float(row[0])
                        temp = float(row[1])
                        qualitylist.append(1)
                    except ValueError:
                        qualitylist.append(0)
                        errornum += 1
                    count += 1
            indictionary[f] = qualitylist
        if errornum > 10:
            badlist.append(f)

    for n in badlist:
        if n in indictionary:
            indictionary.pop(n)

    indictionary['FileNumber'] = len(indictionary) - 1
    return indictionary


if __name__ == "__main__":
    result = filereader()
    print(result)

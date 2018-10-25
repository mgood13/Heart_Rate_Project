import csv
import os


def filereader():
    """The main file reader function.

    :return finaldictionary: The dictionary containing the file names and their dialect for the csv reader
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
                print('Not a csv file')
                errornum = 1

            if errornum == 0:
                outdictionary[f] = dialect
                count += 1
    outdictionary['FileNumber'] = count
    # Return dictionary with file names, delimiter types, and number of valid files
    return outdictionary


def floatcheck(indictionary):
    """Method that checks to ensure all the valid .csv files contain only numbers

    :param indictionary: Dictionary that contains all real .csv file names and their dialect
    :return indictionary: Dictionary containing only the files that contain only numbers
    """
    temp = 0
    badlist = []
    for f in indictionary:
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
                    except ValueError:
                        badlist.append(f)
                        break
    for n in badlist:
        if n in indictionary:
            indictionary.pop(n)

    return indictionary


if __name__ == "__main__":
    result = filereader()
    print(result)

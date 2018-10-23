import csv
import os


def fileReader():
    outdictionary = {}

    files = csvFinder()

    outdictionary = csvChecker(files)
    return outdictionary

def csvFinder():
    # This method finds all files that end in .csv
    files = [f for f in os.listdir('.') if f.endswith(".csv")]
    return files

def csvChecker(files):
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





if __name__ == "__main__":
    result = fileReader()
    print(result)

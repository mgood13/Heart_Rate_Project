import csv
import os


def fileReader():
    errornum = 0
    outdictionary = {}
    templist = []
    count = 0

    files = [f for f in os.listdir('.') if f.endswith(".csv")]
    for f in files:
        with open(f, 'r') as csv1:
            errornum = 0

            try:
                dialect = csv.Sniffer().sniff(csv1.read(), delimiters=',')
            except csv.Error:
                print('Not a csv file')
                errornum = 1

            if errornum == 0:
                outdictionary[f] = dialect
                count += 1


    outdictionary['FileNumber'] = count
    return outdictionary


if __name__ == "__main__":
    result = fileReader()
    print(result)

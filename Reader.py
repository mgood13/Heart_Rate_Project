import csv
import os

def fileReader():
    errornum = 0

    files = [f for f in os.listdir('.') if f.endswith(".csv")]
    for f in files:

        with open(f, 'r') as csv1:
            try:
                dialect = csv.Sniffer().sniff(csv1.read(),delimiters=',')
            except csv.Error:
                print('Not a csv file')
                errornum = 1

            if errornum == 0:
                csv1.seek(0)
                reader = csv.reader(csv1, dialect)
                for row in reader:
                    print(row[0])
                    print(row[1])







if __name__ == "__main__":
    fileReader()
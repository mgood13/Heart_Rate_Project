import csv
from Reader import fileReader

def fileProcessor():
    inputdictionary = fileReader()
    count = 0
    timelist = []
    voltagelist = []

    total = inputdictionary.pop('FileNumber')


    for i in inputdictionary:
        with open(i, 'r') as csv1:
            dialect = inputdictionary.get(i)
            reader = csv.reader(csv1, dialect)
            for row in reader:
                timelist.append(float(row[0]))
                voltagelist.append(float(row[1]))
                count += 1

        timelen = len(timelist)
        maxvolt = max(voltagelist)
        minvolt = min(voltagelist)

        print(maxvolt)
        print(minvolt)

        duration = timelist[timelen-1] - timelist[0]
        print(duration)

if __name__ == "__main__":
    result = fileProcessor()
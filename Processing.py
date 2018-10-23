import csv
from Reader import fileReader

def fileProcessor():
    inputdictionary = fileReader()
    count = 0

    total = inputdictionary.pop('FileNumber')


    for i in inputdictionary:
        count += 1







if __name__ == "__main__":
    result = fileProcessor()
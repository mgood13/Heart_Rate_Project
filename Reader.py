import csv

def fileReader():
    errornum = 0
    with open('test_data1.csv', 'r') as csv1:
        try:
            dialect = csv.Sniffer().sniff(csv1.read(),delimiters=',')
        except csv.Error:
            print("Maybe?")
            errornum = 1

        if errornum == 0:
            csv1.seek(0)
            reader = csv.reader(csv1, dialect)
            for row in reader:
                print(row[0])
                print(row[1])





if __name__ == "__main__":
    fileReader()
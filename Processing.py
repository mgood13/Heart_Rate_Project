import csv
from Reader import fileReader

def fileProcessor():
    inputdictionary = fileReader()
    count = 0
    timelist = []
    voltagelist = []
    diff_vec = []
    scaling = 0.5
    diffmax = 0
    threshold = 0
    beat_time = []

#Determines the number of files that are expected
    total = inputdictionary.pop('FileNumber')

#Loops through each of the files
    for i in inputdictionary:
        with open(i, 'r') as csv1:
            dialect = inputdictionary.get(i)
            reader = csv.reader(csv1, dialect)

            #Populates the lists for time and voltage
            for row in reader:
                timelist.append(float(row[0]))
                voltagelist.append(float(row[1]))
                count += 1
        #Determines the Max and Min voltages
        timelen = len(timelist)
        maxvolt = max(voltagelist)
        minvolt = min(voltagelist)

        #Determines duration of input signal
        duration = timelist[timelen-1] - timelist[0]
        print(duration)

        #Takes the derivative of the signal for the threshold determination

        for x in range(0,timelen):
            if x < (timelen -1):
                diff_vec.append( (voltagelist[x+1] - voltagelist[x]) / (timelist[x+1] - timelist[x]))

        diffmax = max(diff_vec)
        threshold = diffmax * scaling

        #Performs the threshold determination and stores the times of the beats
        count = 0
        for n in range(0, (timelen-1)):
            if x > 1:
                if (diff_vec[n] > threshold and diff_vec[n - 1] < threshold and diff_vec[n-2] < threshold):
                    count = count + 1
                    beat_time.append(timelist[n])


    print(count)
    print(beat_time)

if __name__ == "__main__":
    result = fileProcessor()
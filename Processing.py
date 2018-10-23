import csv
from Reader import fileReader
import numpy as np


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
    metrics = {}

#Determines the number of files that are expected
    total = inputdictionary.pop('FileNumber')

#Loops through each of the files
    for i in inputdictionary:
        with open(i, 'r') as csv1:

            timelist, voltagelist = fileParser(i,csv1, inputdictionary)

        timelen = len(timelist)
        minvolt, maxvolt, duration = ECGMathCalc(timelist, voltagelist, timelen)

        diff_vec = differentiator(timelen, voltagelist, timelist)


        diffmax = max(diff_vec)
        threshold = diffmax * scaling

        beatcount, beat_time = beatCounter(timelen, diff_vec, threshold, timelist)


        metrics['voltage_extremes'] = (minvolt, maxvolt)
        metrics['duration'] = duration
        metrics['num_beats'] = beatcount
        beat_time_array = np.array(beat_time)
        metrics['beats'] = beat_time_array

    return outputdictionary

def fileParser(i, csv1, inputdictionary):
    timelist = []
    voltagelist = []
    count = 0

    dialect = inputdictionary.get(i)
    reader = csv.reader(csv1, dialect)

    # Populates the lists for time and voltage
    for row in reader:
        timelist.append(float(row[0]))
        voltagelist.append(float(row[1]))
        count += 1

    return timelist, voltagelist


def ECGMathCalc(timelist, voltagelist, timelen):
    duration = 0

    #Determines Min and Max voltages in the file
    minvolt = min(voltagelist)
    maxvolt = max(voltagelist)


    # Determines duration of input signal
    duration = timelist[timelen-1] - timelist[0]
    print(duration)
    return minvolt, maxvolt, duration

def differentiator(timelen, voltagelist, timelist):
    # Takes the derivative of the signal for the threshold determination
    diff_vec = []

    for x in range(0, timelen):
        if x < (timelen - 1):
            diff_vec.append((voltagelist[x + 1] - voltagelist[x]) / (timelist[x + 1] - timelist[x]))

    return diff_vec

def beatCounter(timelen, diff_vec, threshold, timelist):
    beatcount = 0
    beat_time = []
    for n in range(0, (timelen - 1)):
        if n > 1:
            if (diff_vec[n] > threshold and diff_vec[n - 1] < threshold and diff_vec[n-2] < threshold):
                beatcount += 1
                beat_time.append(timelist[n])

    return beatcount, beat_time



if __name__ == "__main__":
    result = fileProcessor()
    print(result)
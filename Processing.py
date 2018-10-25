import csv
from Reader import filereader
import numpy as np


def fileProcessor():
    inputdictionary = filereader()
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

        timelist, voltagelist = fileparser(i)


        minvolt, maxvolt, duration, timelen = ecgmathcalc(timelist, voltagelist)

        diff_vec = differentiator(timelen, voltagelist, timelist)


        diffmax = max(diff_vec)
        threshold = diffmax * scaling

        beatcount, beat_time = beatcounter(timelen, diff_vec, threshold, timelist)
        heartrate = heartratecalc(beatcount, beat_time, duration, 0.5)


        metrics['voltage_extremes'] = (minvolt, maxvolt)
        metrics['duration'] = duration
        metrics['num_beats'] = beatcount
        beat_time_array = np.array(beat_time)
        metrics['beats'] = beat_time_array
    return metrics

def fileparser(i):
    timelist = []
    voltagelist = []
    count = 0

    with open(i, 'r') as csv1:
        reader = csv.reader(csv1)

    # Populates the lists for time and voltage
        for row in reader:
            timelist.append(float(row[0]))
            voltagelist.append(float(row[1]))
            count += 1

    return timelist, voltagelist


def ecgmathcalc(timelist, voltagelist):
    duration = 0
    timelen = len(timelist)

    #Determines Min and Max voltages in the file
    minvolt = min(voltagelist)

    maxvolt = max(voltagelist)


    # Determines duration of input signal
    duration = timelist[timelen-1] - timelist[0]
    return minvolt, maxvolt, duration, timelen

def differentiator(timelen, voltagelist, timelist):
    # Takes the derivative of the signal for the threshold determination
    diff_vec = []

    for x in range(0, timelen):
        if x < (timelen - 1):
            diff_vec.append((voltagelist[x + 1] - voltagelist[x]) / (timelist[x + 1] - timelist[x]))

    return diff_vec

def beatcounter(timelen, diff_vec, threshold, timelist):
    beatcount = 0
    beat_time = []
    for n in range(0, (timelen - 1)):
        if n > 1:
            if (diff_vec[n] > threshold and diff_vec[n - 1] < threshold and diff_vec[n-2] < threshold):
                beatcount += 1
                beat_time.append(timelist[n])

    return beatcount, beat_time


def heartratecalc(beatcount, beat_time, duration, usermin=1):
    usersec = usermin * 60
    if (usersec > duration):
        ratio = duration/usersec
        #print("Longer")
        #print(beatcount/ratio/usermin)
    else:
        count = 0
        for n in beat_time:
            if (n < usersec):
                count += 1
        #print("Shorter")
        #print(count/usermin)




if __name__ == "__main__":
    result = fileProcessor()
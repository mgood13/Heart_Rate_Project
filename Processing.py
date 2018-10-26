import csv
from Reader import filereader
import numpy
import json
import os.path


def fileprocessor():
    """The main method that runs the processor function

    This function runs our read program and then runs its own various functions
    it ultimately outputs all the relevant json files named after the csv file
    where the data originated.

    :return metrics: Dictionary containing all the calculated metrics
    """
    inputdictionary = filereader()
    count = 0
    timelist = []
    voltagelist = []
    diff_vec = []

    diffmax = 0
    threshold = 0
    beat_time = []
    metrics = {}

# Determines the number of files that are expected
    total = inputdictionary.pop('FileNumber')

# Loops through each of the files
    for i in inputdictionary:

        qualitylist = inputdictionary[i]
        timelist, voltagelist = fileparser(i, qualitylist)

        minvolt, maxvolt, duration, timelen = \
            ecgmathcalc(timelist, voltagelist)

        diff_vec = differentiator(timelen, voltagelist, timelist)

        beatcount, beat_time = beatcounter(timelen, diff_vec, timelist)
        heartrate = heartratecalc(beatcount, beat_time, duration, 0.5)

        metrics['Original File Name'] = i
        metrics['voltage_extremes'] = (minvolt, maxvolt)
        metrics['duration'] = duration
        metrics['num_beats'] = beatcount
        beat_time_array = numpy.array(beat_time)
        metrics['beats'] = beat_time_array
        metrics['mean_hr_bpm'] = heartrate
        outputstr = jsonout(i, metrics)
    return i, metrics


def fileparser(i, qualitylist):
    """Method that pulls data from input files for use in calculation

    This method takes the file name and a list which was created in the
    file reader which determines the validity of a given line. Basically
    if the line contains bad data then it is discarded in this method. It
    also creates printed output related to the files that it reads. If it
    finds that there was a bad row then it will point this out to the user
    and also print out the number of rows that were discarded. If the ECG
    values are out of bounds (>10mV) then it will inform the user that the
    file in question contains out of bounds data and that the max and min
    will be skewed as a result.

    :param i: The file name
    :param qualitylist: The list with a value for each row, 0-bad, 1-good
    :return timelist: List with the time values
    :return voltagelist: List with the voltage values
    """
    timelist = []
    voltagelist = []
    count = 0

    with open(i, 'r') as csv1:
        abnormal = 0
        discard = 0
        addrow = 0
        reader = csv.reader(csv1)
    # Populates the lists for time and voltage
        for row in reader:
            if qualitylist[count] == 1:
                timelist.append(float(row[0]))
                voltagelist.append(float(row[1]))
                if float(row[1]) > 10:
                    abnormal = 1
            else:
                discard += 1
                count += 1
                continue
            count += 1

        if abnormal == 1:
            print('File %s contains abnormal ECG values, '
                  'max and min may be skewed' % i)
        if discard > 0:
            print('File %s has bad data' % i)
            print('%i lines discarded' % discard)

    return timelist, voltagelist


def ecgmathcalc(timelist, voltagelist):
    """Method that performs the basic math functions

    This method takes the input lists from the fileparser and then obtains
    the basic metrics. These include the max and min and duration. It also
    obtains the length of the time list which is used in later calculations.
    Max and min are both obtained using built in python functions and duration
    is calculated by subtracting the endpoints.

    :param timelist: List of time values
    :param voltagelist: List of voltage values
    :return minvolt: Minimum voltage value recorded
    :return maxvolt: Maximum voltage value recorded
    :return duration: Duration of the ECG recording
    :return timelen: Length of the time list
    """
    duration = 0
    timelen = len(timelist)

    # Determines Min and Max voltages in the file
    minvolt = min(voltagelist)

    maxvolt = max(voltagelist)

    # Determines duration of input signal
    duration = timelist[timelen-1] - timelist[0]
    return minvolt, maxvolt, duration, timelen


def differentiator(timelen, voltagelist, timelist):
    """Method that performs a derivative for beat detection

    This method actually only performs the derivative, the beat detection
    is calculated elsewhere. This is basically just to sharpen the differences
    between the QRS complex and the other parts of the ECG for simpler
    thresholding. This also sort of eliminates the need for accounting for
    low frequency noise because the derivative isn't affected by it. It
    returns values that are derivatives of the original signal.

    :param timelen: Length of the time list
    :param voltagelist: List containing voltage values
    :param timelist: List containing time values
    :return diff_vec: List containing the values of the derivative
    """
    # Takes the derivative of the signal for the threshold determination
    diff_vec = []

    for x in range(0, timelen):
        if x < (timelen - 1):
            diff_vec.append((voltagelist[x + 1] - voltagelist[x]) /
                            (timelist[x + 1] - timelist[x]))

    return diff_vec


def beatcounter(timelen, diff_vec, timelist, scaling = 0.5):
    """Method that performs beat detection from the derivative

    This method uses the derivative list calculated in the previous method
    and performs threshold detection. The threshold is set at a default
    of 0.5 of the max derivative peak but can be adjusted by the user by
    adding an input to the original function call. To ensure that the
    threshold doesn't double count a single peak if it's above the threshold
    for a few values it makes sure that the point that is counted is alone
    and that the previous 2 points are not above threshold. When a beat is
    deteced the time of the beat is placed into a list as well.

    :param timelen: Length of the time list
    :param diff_vec: List containing the derivative values
    :param timelist: List containing the time values
    :return beatcount: The number of beats detected
    :return beat_time: The time of all the beats detected
    """
    beatcount = 0
    diffmax = max(diff_vec)
    threshold = diffmax * scaling
    beat_time = []
    for n in range(0, (timelen - 1)):
        if n > 1:
            if diff_vec[n] > threshold and diff_vec[n - 1] < threshold \
                    and diff_vec[n-2] < threshold:
                beatcount += 1
                beat_time.append(timelist[n])

    return beatcount, beat_time


def heartratecalc(beatcount, beat_time, duration, usermin=1):
    """Method that determines the average heart rate over a given interval

    This method calculates the heart rate based upon a number of minutes given
    when the function is called (with a default of 1 minute). The function
    basically determines if the input number of minutes is longer than the
    duration of the ECG measurement and then creates a ratio between the
    input and the duration. If it is longer than the duration then this ratio
    is multiplied with the total number of beats to get the extrapolated
    heart rate. If the number is shorter than the duration then the function
    runs through the time of all beats to determine how many have passed in
    the given interval to then calculate the heart rate.

    :param beatcount: The number of beats detected
    :param beat_time: The time of all the beats detected
    :param duration: Duration of the ECG recording
    :param usermin: Number of minutes for the HR calculation
    :return avg_hr: The calculated average heart rate
    """
    avg_hr = 0
    usersec = usermin * 60
    if usersec > duration:
        ratio = duration/usersec
        avg_hr = beatcount/ratio/usermin
    else:
        count = 0
        for n in beat_time:
            if n < usersec:
                count += 1
        avg_hr = count/usermin

    return avg_hr


def jsonout(i, metrics):
    """Method that produces the json string and output files

    This method creates a json string and then returns it and also
    prints it to a new file. The printing function takes the name
    of the file the data came from and then clips off the .csv
    ending and doesn't add a new extension. So test1.csv -> test1


    :param i: The file name
    :param metrics: The dictionary containing the calculated metrics
    :return outputstr: The json string
    """
    temp = list(metrics['beats'])
    metrics['beats'] = temp
    outputstr = json.dumps(metrics, indent=4)
    templen = len(i)
    temp = i[0:templen-4]
    filename = temp
    finalfile = os.path.join('./output', filename)
    f = open(finalfile, 'w')
    f.write(outputstr)
    return outputstr


if __name__ == "__main__":
    result = fileprocessor()

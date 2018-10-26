# Heart_Rate_Project


This is the repository containing all of the code for the Heart Rate Monitor Project.
The code is largely broken up into 2 distinct components: Reader.py and Processing.py.
This distinction is larely for the purpose of organizing the commands together under categories
as you don't need to run both of them to get the desired output.
To simply run the program use: *python Processing.py*

Code Function:

**Reader.py** - This function performs all the initial reading and checking for the validity of files
in the current repository. 

First it finds all files ending in .csv and groups them together. Then
it sorts through which of these files are true .csv files. 

Finally it sorts out if any of the
remaining valid files have any abnormal lines. An abnormal line is one where maybe one of the data
values is missing or there is a string (of words not a string like '5'). 

It creates a list for each file that makes it to the end of the Reader.py file and the list contains 
a value for each row of the file. If the value is 1 that row is fine to be passed along. If the value 
is 0 then that row is marked for removal later on in the process. Its ultimate output is a dictionary
containing the file names that passed the checks as keys and the list mentioned above as the value.

**Processor.py**- This function performs the processing and the output for the assignment. First it calls
Reader.py to sort through all of the files in the current folder. It takes the dictionary output and
then parses through to get two lists: time and voltage. It uses the list passed along with the file
names to toss out bad rows. It also notifies the user at this point if any and how many rows were
thrown out and if the values recorded in the lists were inside the normal bounds for an ECG. Then it
calculates the minimum voltage, maximum voltage, and the duration of the recording. 

Next it takes the derivative of the input graph using a simple, discrete slope calculator. 
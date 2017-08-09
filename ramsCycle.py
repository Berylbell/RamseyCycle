#----------------------------------------------------ramsCycle------------------------------------------------------------
#For use with PENTrack as of 06.19.2017
#Generates the file substructure for running a probe over a range of frequencies of a Ramsey Cycle
#Takes input of the template directory, the min and max frequecies, the steps between the min max, and an output directory
#Assumes that the template directory has the 3 PENTrack configuration files
#Assuems that the locations in the geometry.in file that should be changed have the placeholder "InputFrequency"
#Assumes that the STL files are stored in a single higher level directory and not in every subfolder
from __future__ import print_function
import shutil
import os 
import fileinput
import subprocess

def copyAllFromTo (src, dest):
	src_files = os.listdir(src)
	for file_name in src_files:
		full_file_name = os.path.join(src, file_name)
		if (os.path.isfile(full_file_name)):
			shutil.copy(full_file_name, dest)


print("-------------------------------------------------------------------------------------------------------------------------------------------------------\n")
print("-------------------------------------------------------------------------------------------------------------------------------------------------------\n")
print("                                                        Welcome to the Ramsey Cycle Sweeper \n")
print("-------------------------------------------------------------------------------------------------------------------------------------------------------\n")
print("-------------------------------------------------------------------------------------------------------------------------------------------------------\n")
print("This script is designed for use with PENTrack \n")
print("Based on your input, it will create a file system that varies the frequency in a specified range \n")
print("This script relies on your template having all three of the PENTrack configuration files as a template. \n")
print("The template should have all the locations that you want to vary the frequency labled with the string: InputFrequency \n")
print("STL files should be in a single absolute path from the PENTrack executable, they will not be copied into every subfolder \n")
print("Use caution \n")
print("-------------------------------------------------------------------------------------------------------------------------------------------------------\n \n")
print("Please eneter the relevant parameters of your Ramsey Cycle sweep: \n")
startFreq = float(raw_input('Starting Frequency of Ramsey Cycles: \n'))
endFreq = float(raw_input('Ending Frequency of Ramsey Cycles: \n'))
stepNum = int(raw_input('Number of Steps between Start and End Frequencies: \n'))
testName = raw_input('Top Level Directory Name: \n')
print("-------------------------------------------------------------------------------------------------------------------------------------------------------\n")
print("First, the generation of the file system. If your file system already exists and you want to skip to the batch step, please specify: \n")
createFiles = raw_input("Do you want to create the filesystem (y/n)? \n")

if createFiles == "y":
	#Get the relevant input parameters
	templateDir = raw_input('Directory Containing Templates: \n')

	#Make the output directory
	if not os.path.exists(testName):
		os.makedirs(testName)

	#Check to make sure the template exists
	if not os.path.exists(templateDir):
		print('Template Directory Not Found')
		quit()

	stepSize = (endFreq-startFreq)/stepNum

	#Create all the frequency files
	for n in range(0,stepNum+1):
		currentFreq = startFreq + n*stepSize
		print("Creating Directory: Freq"+str(currentFreq))
		currentDir = os.path.join(testName,"Freq"+str(currentFreq))

		if not os.path.exists(currentDir+"_in"):
			os.makedirs(currentDir+"_in")

		if not os.path.exists(currentDir+"_out"):
			os.makedirs(currentDir+"_out")

		copyAllFromTo(templateDir, currentDir+"_in")

		file = fileinput.FileInput(os.path.join(currentDir+"_in","geometry.in"), inplace=True)
		for line in file:
			line= line.replace('InputFrequency', str(currentFreq))
			print (line)
		file.close()
	print('Directories Constructed! \n \n')

#Check if the user wants to make the batch scripts
print("-------------------------------------------------------------------------------------------------------------------------------------------------------\n")
print('If you want, the sciprt will now generate the batch submission scripts. Before saying yes, ensure that preRunCheck.sh is in your folder. \n')
runPreCheck= raw_input("Do you want to run preRunCheck and generate submission files (y/n)? \n")

if runPreCheck == "y":
	#Get Job Parameters
	minJob = int(raw_input("Minimum job number: \n"))
	maxJob = int(raw_input("Maximum job number: \n"))

	#Check if the path exists before running 
	if os.path.exists("preRunCheck.sh"):
		for n in range(0,stepNum+1):
			currentFreq = startFreq + n*stepSize
			currentDir = os.path.join(testName,"Freq"+str(currentFreq))
			subprocess.call("./preRunCheck.sh "+str(minJob)+" "+ str(maxJob)+" Rams"+str(currentFreq)+" "+currentDir+"_in "+currentDir+"_out Rams"+str(currentFreq)+"_batch.pbs", shell=True)
	else:
		print("You didn't check if preRunCheck.sh was in your folder... Its not.")
		quit()

print("-------------------------------------------------------------------------------------------------------------------------------------------------------\n")
print("This would be a good time to check that all the preRunChecks ran as expected. Are all your STL files where they should be? Are you ok with the job overwrites?")
raw_input("Press Enter to Continue...")
print("\n \n-------------------------------------------------------------------------------------------------------------------------------------------------------\n")
print("Batch submission scripts for your cycles have been generated. Would you like them submitted as well? \n")
submitAll = raw_input("Submit all scripts (y/n)? \n")

if submitAll != "y":
	quit()

for n in range(0,stepNum+1):

	currentFreq = startFreq + n*stepSize
	if os.path.exists("Rams"+str(currentFreq)+"_batch.pbs"):
		subprocess.call("qsub Rams"+str(currentFreq)+"_batch.pbs", shell=True)
	else:
		print("Oops, thats weird. batch script for frequency "+ str(currentFreq) +" Doesn't exist. Did you delete it? Or maybe forgot to run the batch generation part of this script?")

print("All the jobs have been submitted. The rest is up to you \n")

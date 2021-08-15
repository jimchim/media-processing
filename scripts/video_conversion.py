import os
import subprocess
from datetime import datetime

print('Enter path to a file containing the full path of the files you want to convert, write one file path on one line each:')

#fileLocation = input()
fileLocation = r"C:\Users\chimk\Desktop\fileList.txt" #debug
exportDirectory = r"C:\Users\chimk\Desktop\converted\%s" %str(datetime.now().strftime("%Y%m%d-%H%M%S"))
# TODOs - turn fileLocation and export directory into relative paths

os.system("mkdir %s" %exportDirectory)
file=open(fileLocation, 'r', encoding="utf-8")

filesToConvert = []

for line in file:
	if line[0] == ":" and line[1] == ":": # this line is a comment
		continue
	else:
		filesToConvert.append(line.strip().strip('\"'))

commands = []
logs=[]


for file in filesToConvert: 
	startTime = str(datetime.now())
	line = "[%s] Converting %s" %(startTime, file)
	logs.append(line+"\n")
	print(line)

	fileName = file.split("\\")
	fileName = fileName[len(fileName)-1]
	fileName = "output-"+fileName

	subprocess.call(['ffmpeg', "-hide_banner", "-loglevel", "quiet", "-stats", '-i', file, '-filter:v', 'scale=1920:-1', '-c:v', 'hevc_amf', '%s\\%s' %(exportDirectory, fileName), "-y"])

	endTime = str(datetime.now())
	line = "[%s] File exported to %s as %s\n" %(endTime, exportDirectory, fileName)
	logs.append(line+"\n")
	print(line)

with open('%s\\conversion.log' %exportDirectory, 'w+',encoding="utf-8") as logFile:
	logFile.writelines(logs)

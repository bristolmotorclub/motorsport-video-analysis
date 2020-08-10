# pip install opencv-python
from cv2 import cv2
import numpy as np
import time
import os

# --- Update these variables ---

# Input file
inputFile = "clip16"
inputFileFormat = ".MP4" #extension
sourceDir = "C:/Users/rodne/Videos/2020DMS/"
# Clip framerate
fps=60

# Path to ffmpeg
ffmpeg = "C:/Users/rodne/Downloads/ffmpeg/bin/ffmpeg.exe"

# Number of frames to skip (more = faster)
skipFrames = 10

# Detection area (number of pixels from top left)
xleft = 860
xright = 1060
ytop = 540
ybottom = 640
# Sensitivity - higher number less sensitive 
pixelCount = 10

# Minimum time interval between clips
minInterval = 0

# ------------------------------

# More variables
outputDir = ""
capture = cv2.VideoCapture(sourceDir + inputFile + inputFileFormat)
print("Opening " + sourceDir + inputFile + inputFileFormat)
xa = xleft/2
xb = xright/2
ya = ytop/2
yb = ybottom/2

# History, Threshold, DetectShadows 
fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

# Keeps track of what frame we're on
frameCount = 0
# keeps track of the seconds we are on
secCount = 0
#writeFlag to decide whether to output to file
lastSecCount = 0
#filename appender
fileCount = 0
skipCount = 0

while(1):
		# Return Value and the current frame
		ret, frame = capture.read()
		
		#  Check if a current frame actually exist
		if not ret:
				break

		skipCount += 1
		frameCount += 1
		secCount = frameCount/fps
		if skipCount > skipFrames:
				# Resize the frame
				resizedFrame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

				# Crop the frame
#				croppedFrame = resizedFrame[290:330,450:510]	#Bobbies tyres
				croppedFrame = resizedFrame[300:400,250:310]	#Bobbies kerb

				# Reset counter
				skipCount = 0
				
				# Get the foreground mask
				fgmask = fgbg.apply(croppedFrame)

				# Count all the non zero pixels within the mask
				count = np.count_nonzero(fgmask)

				print('seconds: %d, Frame: %d, Pixel Count: %d' % (secCount, frameCount, count))
        
				# Determine how many pixels do you want to detect to be considered "movement"
				# if (frameCount > 1 and count > 5000):
				if (frameCount > 1 and count > pixelCount and (secCount - lastSecCount > minInterval)):
						print('---- Car detected ----')
						fileCount +=1
						outputFrame = frame[300:1400,0:1320]
						cv2.imwrite("workingfiles/photos/16-%d.jpg" % fileCount, outputFrame)
						lastSecCount = secCount
				cv2.imshow('Frame', croppedFrame)
				#cv2.imshow('Mask', fgmask)

				k = cv2.waitKey(1) & 0xff
				if k == 27:
						break
capture.release()
cv2.destroyAllWindows()
secondsPerCar = secCount / fileCount
print("Found " + str(fileCount) + " cars [" + str(secondsPerCar) + " seconds per car]")
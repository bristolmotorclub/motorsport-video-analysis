# pip install opencv-python
from cv2 import cv2
import numpy as np
import time
import os

# --- Update these variables ---

# Input file
inputFile = "carvideo"
inputFileFormat = ".MP4" #extension
sourceDir = "C:/path/to/Videos/"
# Clip framerate
fps=60

# Path to ffmpeg
ffmpeg = "C:/path/to/ffmpeg.exe"

# Number of preceeding seconds to clip
offSet = 2.5
# Duration of each clip (seconds)
duration = 7

# Number of frames to skip (more = faster)
skipFrames = 10

# Detection area (number of pixels from top left)
xleft = 860
xright = 1060
ytop = 540
ybottom = 640
# Sensitivity - higher number less sensitive 
pixelCount = 30

# Minimum time interval between clips
minInterval = 5

# ------------------------------

# More variables
outputDir = ""
capture = cv2.VideoCapture(sourceDir + inputFile + inputFileFormat)
print("Opening " + sourceDir + inputFile + inputFileFormat)
xa = xleft/2
xb = xright/2
ya = ytop/2
yb = ybottom/2

# end of env Variables 

#need to check for existence of these files before trying to delete 
#os.remove("workingfiles/timestamps.txt")
#os.remove("workingfiles/ExtractClips.bat")
#os.remove("workingfiles/fileList.txt")
# set output file
output1 = open(sourceDir + "/workingfiles/timestamps.txt","a")
output2 = open(sourceDir + "/workingfiles/ExtractClips.bat","a")
output3 = open(sourceDir + "/workingfiles/fileList.txt","a")


# History, Threshold, DetectShadows 
# fgbg = cv2.createBackgroundSubtractorMOG2(50, 200, True)
fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

# Keeps track of what frame we're on
frameCount = 0
# keeps track of the seconds we are on
secCount = 0
#writeFlag to decide whether to output to file
lastSecCount = 0
#filename appender
fileCount = 0
#print('@echo off \necho start file processing \n')
output2.write('@echo off \necho start file processing \n')
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
		timeStamp = time.strftime('%H:%M:%S', time.gmtime(secCount-offSet))
		#print(timeStamp)
		if skipCount > skipFrames:
				# Resize the frame
				resizedFrame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

				# Crop the frame
				croppedFrame = resizedFrame[290:330,430:530]

				# Reset counter
				skipCount = 0
				
				# Get the foreground mask
				fgmask = fgbg.apply(croppedFrame)

				# Count all the non zero pixels within the mask
				count = np.count_nonzero(fgmask)

				print('seconds: %d, Frame: %d, Pixel Count: %d' % (secCount, frameCount, count))
        
				# Determine how many pixels do you want to detect to be considered "movement"
				# if (frameCount > 1 and cou`nt > 5000):
				if (frameCount > 1 and count > pixelCount and (secCount - lastSecCount > minInterval)):
						print('---- Car detected ----')
						fileCount +=1
						output1.write('seconds: %d, Frame: %d, Pixel Count: %d, timestamp %s \n' % (secCount, frameCount, count, timeStamp))
						output2.write(ffmpeg + ' -i "%s%s.MP4" -vcodec copy -acodec copy -ss %s -t 00:00:%d "workingfiles\\%s%s_%d.MP4" \n' %(sourceDir, inputFile, timeStamp, duration, outputDir, inputFile, fileCount))
						output3.write('file workingfiles/%s%s_%d.MP4 \n' %(outputDir, inputFile, fileCount))
						cv2.imwrite("workingfiles/%d.jpg" % fileCount, frame)
						lastSecCount = secCount
				cv2.imshow('Frame', croppedFrame)
				#cv2.imshow('Mask', fgmask)

				k = cv2.waitKey(1) & 0xff
				if k == 27:
						break
#print('echo files processed \necho now concatenate files \nC:\\Users\\User1\\Downloads\\ffmpeg-20190529-02333fe-win64-static\\ffmpeg-20190529-02333fe-win64-static\\bin\\ffmpeg -f concat -i workingfiles\\fileList.txt -c copy "output_video\\%s%s_combined.MTS"' % (outputDir, inputFile))
output2.write('echo files processed \necho now concatenate files \n' + ffmpeg + ' -f concat -i workingfiles\\fileList.txt -c copy "output_video\\%s%s_combined.MP4"' % (outputDir, inputFile))
output1.close()
output2.close()
output3.close()
capture.release()
cv2.destroyAllWindows()
secondsPerCar = secCount / fileCount
print("Found " + str(fileCount) + " cars [" + str(secondsPerCar) + " seconds per car]")
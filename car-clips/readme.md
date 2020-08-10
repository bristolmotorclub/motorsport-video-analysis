# car-clips
A couple of scripts for pulling car clips out of one single video and stitching together a bunch of videos in a number of sub-folders to join them together with ffmpeg and make one video of all clips in each folder.

## Getting Started

### Prerequisites

* Powershell
* python3
* ffmpeg
* video files that are all the same format

## Usage

### Splitting clips out of one big video
Edit clip-cars-from-video.py to set the raw video, detection area and sensitivity.  Running the script will show the detection area on-screen and the associated sensitivity values.

The script will output ExtractClips.bat and fileList.txt.  When you run ExtractClips.bat, it will extract a video of each car as a separate clip and then create a video of all of them in time order.  Afterwards, you can place the clips of each car into subfolders for stictching together class videos using New-FFmpegFileList.ps1

### Joining folders of clips together
Edit New-FFmpegFileList.ps1 to set the name of the event and the path to ffmpeg (ffmpeg.exe if it's on the path).

Change directory to the folder containing all the folders of clips and run the script.  It will output files.txt in each folder, containing a list of all the files in that folder.  It will also output ffmpeg.bat containing a list of ffmpeg commands to create a video from each list, which it finally executes.
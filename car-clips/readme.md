# car-clips
A script for pulling together a bunch of videos in a number of sub-folders to join them together with ffmpeg and make one video of all clips in each folder

## Getting Started

### Prerequisites

* Powershell
* ffmpeg
* video files that are all the same format

### Installing
Edit New-FFmpegFileList.ps1 to set the name of the event and the path to ffmpeg (ffmpeg.exe if it's on the path).

### Usage
Change directory to the folder containing all the folders of clips and run the script.  It will output files.txt in each folder, containing a list of all the files in that folder.  It will also output ffmpeg.bat containing a list of ffmpeg commands to create a video from each list, which it finally executes.
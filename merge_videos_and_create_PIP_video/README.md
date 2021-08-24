This script is for combining 2 video sources and creating a transcoded video in picture-in-picture mode.

It asks for input from the user, merge the files with FFMPEG, create the video.

It expects the files to be combined to be put into respective folders (e.g. a folder containing all the video files from a front facing camera, and another folder containing all the video files from a rear facing camera.)


### Usage: 
1. Open a terminal (powershell if you are on Windows - make sure python 3 is installed and the PATH is configured)
2. Run `python merge_and_transcode_pip_videos.py`


### NOTE - You should:
1. Make sure you have FFMPEG installed and its PATH properly configured.
2. Make sure the source video files to be put into dedicated folders
3. The 2 source video file folders should contain the same amount of files (the PIP overlay assumes the 2 streams to start and stop at the exact same time).
4. If you have a discrete graphics card available, look up the video encoder you can use with that card (e.g. AMD h.265 encoder is called "hevc_amf" whereas nVidia's is called "hevc_nvenc").
   Using a hardward encoder will significantly boost transcoding performance.
   If none is specified, it will try to use the default - libx264 which is a software encoder
   You may look up the what encoders are available to you with "ffmpeg -encoders"
   
   If you have no idea what an encoder is, just leave it empty.

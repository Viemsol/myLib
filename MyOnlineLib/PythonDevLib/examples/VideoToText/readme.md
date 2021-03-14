# Video to Subtitle Tool (*Vid2Sub*)

## Overview
Tool except any language video or audio file and provide subtitles in desired language.

## How to use Vid2Sub tool
- CLI Command
    - python.exe vid2Sub.py [OPTIONS] FILE
    - **example** python.exe vid2Sub.py [-d -l -f -t] path\to\mp4\or\mp3
    - **d:** Debug prints Enabled
    - **l:** Generate log file 
    - **f:** From Language. if not specified auto detect language
    - **t:** To language, if not specified "en" = English
    - **q:** silent mode info and debug print disabled
- GUI
    - **vid2SubGui.exe** is GUI developed using **CL2UI** Tool
    - ![VidSub User Interface Tool View](/images/VidSubGui.png)
        
## Limitations
- Only **mp4** video and **mp3** audio format supported as input
- Tool have limit to size of video or audio file (Maximum 999 min)
- Tool need Internet connection for Translation

## Dependency
- googletrans==3.1.0a0
- moviepy
- SpeechRecognition
- install **ffmpeg** and **mp3splt** and add path to Environment variables
- Using ffmpeg in CLI for converting video **ffmpeg -i sample.avi -q:a 0 -map a sample.mp3**
## Reference's
- [link to CL2UI Tool!](https://github.com/Viemsol/WindowsTools/tree/master/cl2ui)
- [Conver your cli project to GUI using CL2UI !](https://www.youtube.com/watch?v=NOB4vr5S5zQ)

## Author
Tool Developed by **Saura Urja Tech** [*sauraurjatech@gmail.com*]



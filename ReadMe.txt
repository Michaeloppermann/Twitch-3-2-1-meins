#################
Info
#################
Description: 3-2-1-meins Countdown with UI Interface
Created by: 
Opodeldog - www.twitch.tv/opodeldog
Version: 1.0.0


################
Usage of 3-2-1-meins Countdown
################
This script creates a text files called "Countdown.txt" in the Overlays folder from this script.
You can simply get there by clicking the "Open Overlay Files Folder" on top of the menu on the right side.

For usage add them as textsource in your streaming software (OBS) or just by simply drag'n'drop into it.

### Countdown.txt:
Displays a countdown that counts down ticker growth exponential and after the countdown reaches 0 it will show the text from the "Custom Text after Countdown" textbox.


You can also set the countdown manually by using the commands in the respective area in the Scripts sidebar.
"Set meinsCountdown chat command".

Use "!meinsCountdown" + the amount of Kekse  + the time in minutes you want to set it to.
Example: !meinsCountdown 300 5 (Sets a new countdown to 5 minutes and 300 Kekse)

Use "!meins" to claim the game and stop the countdown.
Example: !meinsCountdown 300 5 (Sets a new countdown to 5 minutes and 300 Kekse)

################
General Installation of Scripts
################
Download the current Streamlabs Chatbot version: https://streamlabs.com/chatbot

Download and install Python 2.7.13 since that's needed for Chatbot and the Script features: 
https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi 

Open the SL Chatbot and go to the "Scripts" tab in the left sidebar.
Click on the cogwheel in the top right and set your Python directory to the `Lib` folder where you installed Python 
(By default it should be `C:\Python27\Lib`).

Click the 'Import' button top right in the "Scripts" tab and select the .zip file you downloaded. It will automatically install the script and move the files into the correct directory.

Afterwards the list of scripts get reloaded and you can start configuring those.


###############
Version History
###############
1.0.0:
  ~ First Release version


###############
(c) Copyright
###############
Opodeldog - www.twitch.tv/opodeldog
All rights reserved. You may edit the files for personal use only.

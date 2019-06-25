# Moon-Mood
Reserching effect of lunar cycle on mood.
Now it's a program under development (it's my fun project or pet-project and used to study PyQT5).
Program objectives are 
  - to represent table for moon and mood data
  - to store and process numerical data (numeric mood scale and moon phases scale) 
  - to represent graph (sinusoid for moon, simple for mood)
  - to average mood-line
  - to request moon data

Current application version realizes all functions above.
Future objectives:
  - calculation optimization of graph painting
  - to implement user-friendly interface

### Installation
You need to have installation folder with MOON.exe if you want to use this application.

### How to use
This application has two areas: table and plot.  You can write your first date in table's column (next date will be set automatically) to start working with the app. You can also write integers between -10 and 10 (try to subjectively rate how was the day). You can change mood data, but you can't change the dates except for the first one.

In plot area you will see two curve lines: mood line and moon phase line. You have ability to display average mood line, when you will have more 20 points and enable this option in checkbox "Average Mood". You can change plot scale: hold CTRL key and move mouse wheel.

You can save your data or open file you previously saved or start a new one. You can copy (CTRL + C) or paste some data in table (date in first column and integer value in second one) if you need.

#### Screenshots
![screenshot of sample](https://pp.userapi.com/c852132/v852132430/155206/_DVUG0mQyWY.jpg)
![screenshot of sample](https://pp.userapi.com/c852132/v852132430/15520f/edWtjGI5Cvg.jpg)
![screenshot of sample](https://pp.userapi.com/c852132/v852132430/155229/pcR3dbn2gRI.jpg)

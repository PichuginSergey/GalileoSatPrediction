# GalileoSatPrediction
This program allows you to calculate the visible Galileo satellites by the almanac. The almanac are taken from 
https://www.gsc-europa.eu/system-status/almanac-data by .xml format.
Program may predict visible Galileo satellites for current date and time or for all current day with step 1 minute.
First, you need to set config.cfg file. 
In this file: x,y,z - reference point, meter; 
elv - elevation mask, degree; 
alm - name of almanac file; 
dayPrediction - switch between now moment predict or all current day predict (Off/On);
out - output file name.

For example
x=2845301
y=2203651
z=5247292
elv=5
alm=2017-10-06.xml
dayPrediction=On
out=res.txt

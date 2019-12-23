# Adapted by Jake Mizzell from JJSilva's NeoSectional Github Repo
from __future__ import print_function
import urllib2
import xml.etree.ElementTree as ET
from neopixel import *
import sys
import os
import time
import subprocess
from neopixel import *


# LED strip configuration:
LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 10     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

strip.begin()

with open("/LiveSectional/airports") as f:
    airports = f.readlines()
airports = [x.strip() for x in airports]
print("Pulling the following airports: ")
print(list(filter(lambda a: a!="NULL", airports)))

mydict = {
        "":""
}

url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=1.5&stationString="
for airportcode in airports:
        if airportcode == "NULL":
                continue
        url = url + airportcode + ","

content = urllib2.urlopen(url).read()
root = ET.fromstring(content)

print("Information downloaded")

for metar in root.iter('METAR'):
        if airportcode == "NULL":
                continue
        stationId = metar.find('station_id').text
        if metar.find('flight_category') is None:
		continue
        flightCateory = metar.find('flight_category').text
        if stationId not in mydict:
                mydict[stationId] = flightCateory

print("\n\nUpdating the lights")

i = 0
for airportcode in airports:
        if airportcode == "NULL":
                i = i + 1
        	continue

 	color = Color(0,0,0)

        flightCateory = mydict.get(airportcode,"No")
        if  flightCateory != "No":
                if flightCateory == "VFR":
                        color = Color(255,0,0)
                elif flightCateory == "MVFR":
                        color = Color(0,0,255)
                elif flightCateory == "IFR":
                        color = Color(0,255,0)
                elif flightCateory == "LIFR":
                        color = Color(0,128,128)
        else:
                color = Color(8,8,8)
                print(airportcode + " N/A")
        print("Setting light " + str(i) + " for " + airportcode + " " + flightCateory + " " + str(color))
	strip.setPixelColor(i, color)
        strip.show()

        i = i + 1

#Uncomment out the following lines to create a Map Legend be sure to also change the numbers to coorispond with your LED light positions.

#print "Setting light 70  for Green " + str(Color(255,0,0))
#strip.setPixelColor(70, Color(255,0,0))
#strip.show()
#print "Setting light 71 for Blue " + str(Color(0,0,255))
#strip.setPixelColor(71, Color(0,0,255))
#strip.show()
#print "Setting light 72 for Red " + str(Color(0,255,0))
#strip.setPixelColor(72, Color(0,255,0))
#strip.show()
#print "Setting light 73 for Pink " + str(Color(0,128,128))
#strip.setPixelColor(73, Color(0,128,128))
#strip.show()
#print "Setting light 74 for White " + str(Color(0,0,0))
#strip.setPixelColor(74, Color(255,255,255))
#strip.show()
#print
#print

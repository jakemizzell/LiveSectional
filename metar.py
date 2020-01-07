# Adapted by Jake Mizzell from JJSilva's NeoSectional Github Repo
import urllib2
import xml.etree.ElementTree as ET
import time
from neopixel import *
import sys
import os
import datetime

#setup for IC238 Light Sensor for LED Dimming, does not need to be commented out if sensor is not used
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)


# LED strip configuration:
LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 10     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

#User defined items to be set
max_wind_speed = 15      #Any speed above will flash the LED for the appropriate airport
toggle = 0      #initialize blink toggle. 0 will start the lights in the ON position. 1 will start with lights OFF.
blink_pause = .8    #Determines how quickly the LED's blink if winds are more than max_wind_speed in seconds
lghtnon = .08       #Lightning on interval in seconds
lghtnoff = .12      #Lightning off interval in seconds
update_interval = 15    #Number of MINUTES between FAA updates - 15 minutes is a good compromise

            #Set LED Colors. Change numbers in paranthesis. The order is (Green,Red,Blue). Each has a range of 0-255.
color_vfr = Color(255,0,0)  #Full bright Green
color_mvfr = Color(0,0,255) #Full bright Blue
color_ifr = Color(0,255,0)  #Full bright Red
color_lifr = Color(0,255,255)   #Full bright Magenta
color_nowx = Color(200,200,200) #Slightly dimmed white
color_black = Color(0,0,0)  #Black/Off
color_yellow = Color(255,255,0) #Full bright Yellow (used for legend on lightning/thunderstorms)

hiwindblink = 1     #1 = Yes, 0 = No. Blink the LED for high wind Airports.
lghtnflash = 1      #1 = Yes, 0 = No. Flash the LED for an airport reporting severe weather like TSRA.

dimmed_value = 10
birght_value = 10

            #list of METAR weather categories to designate severe weather in area.
            #See https://www.aviationweather.gov/metar/symbol for descriptions. Add or subtract as necessary.
wx_lghtn_ck = ["TS", "TSRA", "TSGR", "+TSRA", "VCSS", "FC", "SQ", "VCTS", "VCTSRA", "VCTSDZ", "LTG"]
iterations = 6      #Number of times that the rainbow animation will run before updating LED colors

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

strip.begin()

#Rainbow Animation functions - taken from https://github.com/JJSilva/NeoSectional/blob/master/metar.py
def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
                return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
                pos -= 85
                return Color(255 - pos * 3, 0, pos * 3)
        else:
                pos -= 170
                return Color(0, pos * 3, 255 - pos * 3)

def rainbowCycle(strip, iterations, wait_ms=2):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
                for i in range(strip.numPixels()):
                        strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
                strip.show()

#Start of infintite loop that first updates data from FAA. Then cycles through the LED's to set colors and blinks as necessary
hour = datetime.datetime.now().hour
while (hour >= 9 and hour <= 17):
    rainbowCycle(strip, iterations)

    #Set all the colors to black
    for number in range(LED_COUNT):
        color = color_black
        strip.setPixelColor(LED_COUNT,color)
        trip.show()
    
    print ("Updating FAA Weather Data") #Debug

    #read airports file
    with open("/LiveSectional/airports") as f:
            airports = f.readlines()
    airports = [x.strip() for x in airports]

    #define dictionaries
    mydict = {
        "":""
    }
    mydictwinds = {
        "":""
    }
    mydicttsra = {
        "":""
    }

    #define URL to get weather METARS. This will pull only the latest METAR from the last 2.5 hours. If no METAR reported withing the last 2.5 hours, Airport LED will be white.
    url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=2.5&stationString="

    #build URL to submit to FAA with the proper airports from the airports file
    for airportcode in airports:
            if airportcode == "NULL":
                    continue
            url = url + airportcode + ","

    try: #Simple Error trap, in case FAA web site is not responding
        #print url #Debug
        content = urllib2.urlopen(url).read()
    except: #End of Error trap
        pass

    root = ET.fromstring(content)

    #grab the airport category, wind speed and TSRA from the results given from FAA.
    for metar in root.iter('METAR'):
        if airportcode == "NULL": #if airport code is NULL, then bypass
            continue
        stationId = metar.find('station_id').text

        #grab flight category from returned FAA data
        if metar.find('flight_category') is None: #if category is blank, then bypass
            continue
        flightCateory = metar.find('flight_category').text

        #grab wind speeds from returned FAA data
        if metar.find('wind_speed_kt') is None: #if wind speed is blank, then bypass
            continue
        windspeedkt = metar.find('wind_speed_kt').text

        #grab Thunderstorm info from returned FAA data
        if metar.find('wx_string') is None: #if weather string is blank, then bypass
            wxstring = "NONE"
        else:
            wxstring = metar.find('wx_string').text

        print stationId + " " + flightCateory + " " + windspeedkt + " " + wxstring #Debug


        #Check for duplicate airport identifier and skip if found, otherwise store in dictionary
        if stationId in mydict:
            print ("Duplicate, only saved first metar category")
        else:
            mydict[stationId] = flightCateory #build category dictionary

        if stationId in mydictwinds:
            print ("Duplicate, only saved the first winds")
        else:
            mydictwinds[stationId] = windspeedkt #build windspeed dictionary

        if stationId in mydicttsra:
            print ("duplicate, only saved the first weather")
        else:
            mydicttsra[stationId] = wxstring #build thunderstorm dictionary

    #Setup timed loop that will run based on the value of update_interval which is a user setting
    timeout_start = time.time()
    while time.time() < timeout_start + (update_interval * 60): #take update interval which is in mins and turn into seconds

        toggle = not(toggle) #used to determine if LED should be on or off


        #Bright light will provide a low input (0). Dark light will provide a high input (1). Full brightness used if no light sensor installed
        if GPIO.input(4) == 1:
                LED_BRIGHTNESS = dimmed_value
        else:
                LED_BRIGHTNESS = birght_value
        strip.setBrightness(LED_BRIGHTNESS)

        #start main loop to determine which airports should blink
        i = 0
        for airportcode in airports:
            if airportcode == "NULL": #retrieve the color that the LED has been assigned so we can save it for restoring if the LED will be Blinking
                color = color_black
                strip.setPixelColor(i, color)
                i = i + 1
                continue

            elif airportcode == "LGND":
                i = i +1
                continue

            flightCateory = mydict.get(airportcode,"No")

            if flightCateory == "VFR":
                color = color_vfr
            elif flightCateory == "MVFR":
                color = color_mvfr
            elif flightCateory == "IFR":
                color = color_ifr
            elif flightCateory == "LIFR":
                color = color_lifr
            else:
                color = color_nowx

            strip.setPixelColor(i, color)

            #Check the windspeed to determine if the LED should blink
            if hiwindblink: #Check user setting to determine if the map should blink for high winds or not
                windspeedkt = mydictwinds.get(airportcode,"No")

                if windspeedkt != "No":
                    if int(windspeedkt) > max_wind_speed:
                        if toggle == 0:
                            blink = color_black #Turn off LED
                            strip.setPixelColor(i, blink)
                        else:
                            blink = color #Turn on LED
                            strip.setPixelColor(i, blink)

            #Check to see if wxstring shows a thunderstorm. Flash LED White randomly if so
            if lghtnflash: #Check user setting to determine if the map should lightning flash for severe weather or not
                wxstring = mydicttsra.get(airportcode,"No")

                if wxstring <> "NONE" or "NO" or "No":

                    if wxstring in wx_lghtn_ck:
                        #quickly flash bright yellow to represent lightning
                        strip.setPixelColor(i, color_yellow)
                        strip.show()
                        time.sleep(lghtnon)
                        strip.setPixelColor(i, color)
                        strip.show()
                        time.sleep(lghtnoff)
                        strip.setPixelColor(i, color_yellow)
                        strip.show()
                        time.sleep(lghtnon)
                        strip.setPixelColor(i, color)
                        strip.show()

            i = i + 1 #increment to next airport

        strip.show()

#if it's outside of the defined time
print("Killing the lights")
for number in range(LED_COUNT):
    color = color_black
    strip.setPixelColor(LED_COUNT,color)
    strip.show()

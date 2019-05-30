# Adapted by Jake Mizzell from JJSilva's NeoSectional Github Repo

from __future__ import print_function
import urllib2
import xml.etree.ElementTree as ET
from neopixel import *
import sys
import os
import time
from neopixel import *


# LED strip configuration:
LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 15     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

strip.begin()

print("Killing the lights")

for number in range(LED_COUNT):
	color = Color(128,128,128)
	strip.setPixelColor(LED_COUNT,color)
	strip.show()


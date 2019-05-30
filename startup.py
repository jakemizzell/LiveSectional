# Written by Jake Mizzell
# This is ran each time the Pi is rebooted
# It determines if the lights turn on or off based on the current time

import datetime

if datetime.datetime.now().hour <= 2 or datetime.datetime.now().hour >= 14:
	print ("Turning on Lights!")
	import metar
else:
	print ("Turning off Lights!")
	import end

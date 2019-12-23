# Written by Jake Mizzell
# This is ran each time the Pi is rebooted
# It determines if the lights turn on or off based on the current time

import subprocess
import datetime
import time

#datetime.datetime.now.hour returns the hour in zulu
#time.localtime().tm_isdst returns 1 if Daylight Savings Time (DST) is in effect otherwise 0
hour = datetime.datetime.now().hour - time.localtime().tm_isdst

#This script should run 9am-5pm Central Time year round if my logic is right
if hour >= 15 and hour <= 22:
	subprocess.Popen(['python','/LiveSectional/rainbow.py']).wait()

	file = open("/LiveSectional/log.txt","a")
	file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Turning on Lights!    ")
	file.close()

	subprocess.Popen(['python','/LiveSectional/metar.py']).wait()
else:
	file = open("/LiveSectional/log.txt","a")
	file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Turning off Lights!    ")
	file.close()

	subprocess.Popen(['python','/LiveSectional/end.py']).wait()

file = open("/LiveSectional/log.txt","a")
file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Finished Script\n")
file.close()

# LiveSectional

This is a Repo I adapted from https://github.com/JJSilva/NeoSectional to create  a Live sectional.
I got this project idea from http://www.iflymn.com/2019/07/livesectional/.

White Lights = Issue with the weather station
Green Lights = VFR
Blue Lights = MVFR
Red Lights = IFR
Purple Lights = LIFR
Flashing Lights = Winds > 15kts

Login  
Username: pi  
Password: livesectional

To change the Wifi information you have to type `sudo raspi-config` and then mess with the network options

Everything lives in a folder called LiveSectional (In the link above he always references it as “NeoSectional”, I renamed the folder and possibly other files)

To get to it the directory type the Command `cd /LiveSectional`

The files (you can see their contents by typing `nano FILENAME`)
* airports – this has all the airport names that are looked up when the script is run. The order of them is very important and this file probably shouldn’t be messed with
* metar.py – this does all of the work. It reads the airports from the “airports” file then looks up all of them on the internet and sets the colors
* startup.sh – this runs metar.py at startup of the pi

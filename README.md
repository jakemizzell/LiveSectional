# LiveSectional

This is a Repo I adapted from [This Repo](https://github.com/JJSilva/NeoSectional) to create  a Live sectional.
I got this project idea from [This blog](http://www.iflymn.com/2019/07/livesectional/).

Login  
Username: pi  
Password: livesectional

To change the Wifi information you have to type `sudo raspi-config` and then mess with he network options

Everything lives in a folder called LiveSectional (In the link above he always references it as “NeoSectional”, I renamed the folder and possibly other files)

To get to it the directory type the Command `cd /LiveSectional`

The files (you can see their contents by typing `nano FILENAME`)
* airports – this has all the airport names that are looked up when the script is run. The order of them is very important and this file probably shouldn’t be messed with
* end.py – this is run to turn off all the lights
* log.txt – I wrote this for when trouble shooting issues. It should be written to each time the script runs
* metar.py – this does most of the work. It reads the airports from the “airports” file then looks up all of them on the internet and sets the colors
* rainbow.py – this makes the lights animate
* startup.py – I wrote this to manage the order when things are ran. It checks the time and then turns the lights on or off depending on the time.

startup.py is run every 15 minutes by the crontab. To adjust how often it is run or anything in crontab run `sudo crontab -e`


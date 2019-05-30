# LiveSectional

This is a Repo I adapted from [This Repo](https://github.com/JJSilva/NeoSectional) to create  a Live sectional.

I added the following lines to my crontab (Acessed by "sudo crontab -e)

```
@reboot python /LiveSectional/starup.py &
*/15 0-2,14-23 * * * python /LiveSectional/starup.py
```
That makes starup.py run at starup and every 15 minutes from 0800-2100 CDT

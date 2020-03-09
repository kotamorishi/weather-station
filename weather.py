from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import Image, ImageFont, ImageDraw, ImageOps
import time
import datetime
import subprocess
import json
import os
import sys


# Settings - please update following.
delay = 2
refresh_interval = 600 # refresh every 600 seconds(10 minuites)
ttf = '/usr/share/fonts/8-Bit Madness.ttf'

serial = i2c(port=1, address=0x3c)
device = ssd1306(serial)
font60 = ImageFont.truetype(ttf, 60)
font42 = ImageFont.truetype(ttf, 42)
font36 = ImageFont.truetype(ttf, 32)
font20 = ImageFont.truetype(ttf, 32)
font12 = ImageFont.truetype(ttf, 16)

def main():
    print("Weather station started")
    
    started_time = time.time() - refresh_interval
    
    while True:
        basedir = os.path.dirname(os.path.realpath(__file__))
        icondir = os.path.join(basedir, 'icons')
        elapsed_time = time.time() - started_time
        
        try:
            if(elapsed_time >= refresh_interval):
                started_time = time.time()
                with canvas(device) as drawUpdate:
                    dlIcon = Image.open(os.path.join(icondir,  "updating.bmp"))
                    drawUpdate.bitmap((32,-6), dlIcon, fill=1)
                    drawUpdate.text((32,52), "Updating", font=font12, fill=255)

                subprocess.check_output(os.path.join(basedir, 'download.sh'), shell=True)
                time.sleep(1) # to prevent flickering
            
            with open(os.path.join(basedir, 'current-data.json')) as conditions_data_file:
                conditions_data = json.load(conditions_data_file)
            
            with open(os.path.join(basedir, 'forecast-data.json')) as forecast_data_file:
                forecast_data = json.load(forecast_data_file)

            city_name = conditions_data[u'name']
            temp_cur = conditions_data[u'main'][u'temp']
            icon = str(conditions_data[u'weather'][0][u'icon'])
            icon = icon[0:2]   # just get first 2 bytes
            humidity = conditions_data[u'main'][u'humidity']
            wind = str(conditions_data[u'wind'][u'speed'])
            wind_dir = str(conditions_data[u'wind'][u'deg'])
            epoch = int(conditions_data[u'dt'])
            utime = time.strftime('%H:%M', time.localtime(epoch))

            logo = Image.open(os.path.join(icondir,  icon + ".bmp"))
            
            
            with canvas(device) as currentWether:
                currentWether.bitmap((48,-6), logo, fill=1)
                currentWether.text((0,0), city_name, font=font12, fill=255)
                currentWether.text((0,22),  "%2.0f" % temp_cur, font=font20, fill=255)
                now = datetime.datetime.now()
                currentWether.text((0,55), now.strftime('%h') + " " + "%2d" % now.day, font=font12, fill=255)
                currentWether.text((94,55), "%02d" % now.hour + ":" + "%02d" % now.minute, font=font12, fill=255)
                #currentWether.text((94,0),  "%2.0f" % humidity + "%", font=font12, fill=255)
            time.sleep(delay)

            # forecast draw : fi = forecast index (every 3 hours)
            for fi in range(2):
                forecast_time_dt  = forecast_data[u'list'][fi][u'dt']
                forecast_time     = time.strftime('%-I%p', time.localtime(forecast_time_dt))
                forecast_temp     = forecast_data[u'list'][fi][u'main'][u'temp']
                forecast_humidity = forecast_data[u'list'][fi][u'main'][u'humidity']
                forecast_icon     = forecast_data[u'list'][fi][u'weather'][0][u'icon'] # show the first wether condition...?
                forecast_bmp      = Image.open(os.path.join(icondir,  forecast_icon[0:2] + ".bmp"))
                with canvas(device) as forecastWether:
                    forecastWether.bitmap((48,-6), forecast_bmp, fill=1)
                    forecastWether.text((0,0), forecast_time, font=font12, fill=255)
                    forecastWether.text((0,22),  "%2.0f" % forecast_temp, font=font20, fill=255)
                    #forecastWether.text((24,14), "c", font=font12, fill=255)
                    #forecastWether.text((0,14),  "%2.0f C" % forecast_temp, font=font12, fill=255)
                    #forecastWether.text((0,28),   str(forecast_humidity) + "%", font=font12, fill=255)
                    now = datetime.datetime.now()
                    forecastWether.text((0,55), now.strftime('%h') + " " + "%2d" % now.day, font=font12, fill=255)
                    forecastWether.text((94,55), "%02d" % now.hour + ":" + "%02d" % now.minute, font=font12, fill=255)
                time.sleep(delay)
        except:
            
            for i in range(30):
                with canvas(device) as drawError:
                    dlIcon = Image.open(os.path.join(icondir,  "unknown.bmp"))
                    drawError.bitmap((32,-12), dlIcon, fill=1)
                    if i % 2 == 0:
                        drawError.text((18,42), "Error occured.", font=font12, fill=255)
                    else:
                       drawError.text((28,42), "Retry in " + str(30 - i), font=font12, fill=255)
                    now = datetime.datetime.now()
                    drawError.text((0,55), now.strftime('%h') + " " + "%2d" % now.day, font=font12, fill=255)
                    drawError.text((94,55), "%02d" % now.hour + ":" + "%02d" % now.minute, font=font12, fill=255)
                    time.sleep(1)
            started_time = time.time() - refresh_interval


if __name__ == "__main__":
    main()




# -*- coding: utf-8 -*-

import grovepi
import grove_rgb_lcd as lcd
import grovegps
import time
import picamera
import atexit
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime,timedelta

###############################################
@atexit.register
def cleanup():
	fobj.close()
	grovepi.digitalWrite(led,0)
	lcd.setText("")
###############################################
	
overlay_txt_ypos = 440
#degree_sign= u'\N{DEGREE SIGN}'
g = grovegps.GROVEGPS()
cam = picamera.PiCamera()
print "time.altzone %d " % time.altzone
photo_location = "./"
logfile="trip.csv"
led = 3
dht_sensor_port = 7
dht_sensor_type = 0
temp = 0
hum = 0
use_lcd = True  # if lcd display is used for feedback

# get a font
fnt = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Thin.ttf', 20)

def display(in_str,bgcol=(255,255,255),in_lcd=use_lcd):
	print(in_str)
	if in_lcd:
		lcd.setRGB(bgcol[0],bgcol[1],bgcol[2])
		lcd.setText(in_str)

def format_coord(in_lat, in_lon):
	'''
	TBD:
	takes in a latitude and a longitude in 
	returns a nicely formatted string in degrees minutes seconds
	'''
	out_lat = in_lat
	out_lon = in_lon
	return (out_lat, out_lon)

def handlegpsdata():
	'''
	Read GPS
	if we get valid data, blink the LED, return True
						and save the info
	else return False
	'''

	g.read()
	if g.lat != -1.0:
		display( "valid",in_lcd=False)
		return True

	display( "invalid",in_lcd=False)
	return False
	
def handledhtdata():
	global temp, hum
	[ temp, hum ] = grovepi.dht(dht_sensor_port,dht_sensor_type)
	display("temp = {}C    humidity={}%".format(temp,hum),(0,255,0))

def logtofile():
	fobj = open( logfile,"a")
	fobj.write("{:.4f}, {:.4f}, {}, {:.2f}, {:.2f}%\n".format(
		g.latitude,g.longitude, g.timestamp, temp,hum))
	fobj.flush()
	fobj.close()

	# handle time. Convert according to timezone
	# convert timestamp to struct_time
	#my_time = time.strptime(g.timestamp,"%H%M%S.000")  
	#print my_time

def savephoto():
	photoname = photo_location+str(g.timestamp)+".jpg"
	display( photoname,in_lcd=False)
	cam.capture(photoname)
	grovepi.digitalWrite(led,0)
	time.sleep(1)
	grovepi.digitalWrite(led,255)
		
	# Get ready to watermark the image
	
	# 1. grab the image
	base = Image.open(photoname).convert('RGBA')

	# 2. create overlay
	txt = Image.new('RGBA', base.size, (255,255,255,50))
	# get a drawing context
	d = ImageDraw.Draw(txt)

	# 3. prepare text to overlay
	d.text((20,overlay_txt_ypos), 
		"lon: {:.4f} lat: {:.4f} temp: {:.1f}C humidity: {:.1f}%".format(
		g.longitude,g.latitude, temp,hum), font=fnt, fill=(255,255,255,255))
	
	# 4. do composite and save
	out = Image.alpha_composite(base, txt)
	out.save(photoname)
	grovepi.digitalWrite(led,255)




###############################################################

fobj = open( logfile,"a")

grovepi.digitalWrite(led,255)
while True:

	if handlegpsdata():
		display("{} {}, {} {}, {}, {}".format(g.lat,g.NS,g.lon,g.EW, g.latitude,g.longitude),
			in_lcd=False)
		handledhtdata()
		savephoto()
		logtofile()
		time.sleep(5)
		display("lon: {:11.7f}lat: {:11.7f}".format(g.longitude,g.latitude),(0,0,255))
	time.sleep(5)



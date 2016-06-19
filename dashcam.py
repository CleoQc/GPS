# -*- coding: utf-8 -*-

import grovepi
import grovegps
import time
import picamera
import atexit
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime,timedelta

@atexit.register
def cleanup():
	fobj.close()
	grovepi.digitalWrite(led,0)
	
overlay_txt_ypos = 440
degree_sign= u'\N{DEGREE SIGN}'

g = grovegps.GROVEGPS()
cam = picamera.PiCamera()
print "time.altzone %d " % time.altzone
photo_location = "/home/pi/Grove_GPS/"
logfile="trip.csv"
led = 3

# get a font
fnt = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Thin.ttf', 20)

def format_coord(in_lat, in_lon):
	'''
	takes in a latitude in 
	returns a nicely formatted string in degrees minutes seconds
	'''


fobj = open( logfile,"a")

grovepi.digitalWrite(led,255)
while True:
	g.read()
	grovepi.digitalWrite(led,50)
	print(g.lat,g.NS,g.lon,g.EW, g.latitude,g.longitude)
	if g.lat != -1.0:
		fobj.write("%.4f, %.4f, %s\n"%(g.latitude,g.longitude, g.timestamp))
		fobj.flush()

		# handle time. Convert according to timezone
		my_time = time.strptime(g.timestamp,"%H%M%S.000")  # convert timestamp to struct_time
		print my_time
		photoname = photo_location+str(g.timestamp)+".jpg"
		print photoname
		cam.capture(photoname)
			
		# Get ready to watermark the image
		
		# 1. grab the image
		base = Image.open(photoname).convert('RGBA')
	
		# 2. create overlay
		txt = Image.new('RGBA', base.size, (255,255,255,0))
		# get a drawing context
		d = ImageDraw.Draw(txt)
	
		# 3. prepare text to overlay
		d.text((20,overlay_txt_ypos), "lon: %.4f lat: %.4f"%(g.longitude,g.latitude), font=fnt, fill=(255,255,255,255))
	
		# 4. do composite and save
		out = Image.alpha_composite(base, txt)
		out.save(photoname)
		grovepi.digitalWrite(led,255)

	time.sleep(10)



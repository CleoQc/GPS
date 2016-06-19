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
	
overlay_txt_ypos = 440
degree_sign= u'\N{DEGREE SIGN}'

g = grovegps.GROVEGPS()
cam = picamera.PiCamera()
print "time.altzone %d " % time.altzone
photo_location = "/home/pi/gps_project/"
# get a font
fnt = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Thin.ttf', 20)

def format_coord(in_lat, in_lon):
	'''
	takes in a latitude in 
	returns a nicely formatted string in degrees minutes seconds
	'''


fobj = open('trip.txt',"a")

while True:
	g.read()
	print(g.lat,g.NS,g.lon,g.EW, g.latitude,g.longitude)
	fobj.write("%.4f\t%.4f\n"%(g.latitude,g.longitude))
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
	d.text((20,overlay_txt_ypos), "lon: %.4f "%g.longitude, font=fnt, fill=(255,255,255,255))
	d.text((140,overlay_txt_ypos), "lat: %.4f"%g.latitude, font=fnt, fill=(255,255,255,255))
	
	# 4. do composite and save
	out = Image.alpha_composite(base, txt)
	out.save(photoname)

	time.sleep(10)



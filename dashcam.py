import grovepi
import grovegps
import time
import picamera

g = grovegps.GROVEGPS()
cam = picamera.PiCamera()
mytimezone = "EDT"
print "time.altzone %d " % time.altzone

while True:
	g.read()
	print(g.lat,g.NS,g.lon,g.EW, g.latitude,g.longitude)

	# handle time. Convert according to timezone
	my_time = time.strptime(g.timestamp,"%H%M%S.000")  # convert timestamp to struct_time
	print my_time
	cam.capture("/home/pi/gps_project/"+ str(g.timestamp) + ".jpg")
	time.sleep(60)



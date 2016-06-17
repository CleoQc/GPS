# -*- coding: utf-8 -*-

import grovepi
import serial, time, sys

degree_sign= u'\N{DEGREE SIGN}'
ser = serial.Serial('/dev/ttyAMA0', 9600,  timeout=0)
ser.flush()

class GPS:
	def __init__(self,port='/dev/ttyAMA0',baud=9600,timeout=0):
		self.ser = serial.Serial(port,baud,timeout=timeout)
		self.ser.flush()
		self.raw_line = ""
		self.gga = ""
		self.atleastone = False

	def read(self):
		while True:
			time.sleep(0.5)
			self.raw_line = self.ser.readline().strip()
			if self.validate(self.raw_line):
				break;
		return self.gga

	def validate(self,in_line):
		if in_line == "":
			return False
		if in_line[:6] != "$GPGGA":
			return False
		self.gga = in_line.split(",")
		try:
			ind=self.gga.index('$GPGGA',5,len(self.gga))	#Sometimes multiple GPS data packets come into the stream. Take the data only after the last '$GPGGA' is seen
			self.gga=self.gga[ind:]
		except ValueError:
			pass
		if len(self.gga) != 15:
			print "Failed"
			print self.gga
			if self.atleastone:
				sys.exit(-1)
			return False

		self.atleastone = True
		return True


gps = GPS()
while True:
	time.sleep(1)
	in_data = gps.read()
	print "Valid",in_data

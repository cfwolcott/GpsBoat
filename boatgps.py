#!/usr/bin/python

# GPS Boat Project - January 2014

# This module will provide an interface to the GPS related functions

import time
import os
import sys
import gps
import math

class BoatGps:

	# -----------------------------
	def __init__(self):
		# Initialize GPS receiver
		self.Locked = False

	#--------------------------------------------------------------------
	# Returns distance from origin (lat1, lon1) to target location (lat2, lon2)
	def CalcDistance( self, lat1, lon1, lat2, lon2 ):
		# Haversine method
		# earth mean Radius
		#R = 6378.1 # km
		R = 3963.19 # mi

		dLat = math.radians(lat2 - lat1)
		dLon = math.radians(lon2 - lon1)
		lat1 = math.radians(lat1)
		lat2 = math.radians(lat2)

		a = math.sin(dLat / 2) * math.sin(dLat / 2) \
			+ math.cos(lat1) * math.cos(lat2) \
			* math.sin(dLon /2) * math.sin(dLon / 2);
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

		return R * c

	#--------------------------------------------------------------------
	# Returns compass bearing from origin (lat1, lon2) to target location (lat2, lon2)
	def CalcBearing( self, lat1, lon1, lat2, lon2 ):
		dLon = math.radians(lon2 - lon1)
		lat1 = math.radians(lat1)
		lat2 = math.radians(lat2)

		y = math.sin(dLon) * math.cos(lat2)
		x = math.cos(lat1) * math.sin(lat2) \
			- math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
		theta = math.degrees( math.atan2(y, x) )
		return (theta + 360.0) % 360.0


#--------------------------------------------------------------------
def main(argv):

	print "Boat GPS Test"
	
	g = BoatGps()

	while True:
		lat1 = input("Enter point A Lat (0 to exit): ")
		if lat1 == 0:
			exit()
		long1 = input("Enter point A Long: ")
		lat2 = input("Enter point B Lat: ")
		long2 = input("Enter point B Long: ")

		distance = g.CalcDistance( lat1, long1, lat2, long2 )
		print "  Distance: " + str(distance) + " miles"

		bearing = g.CalcBearing( lat1, long1, lat2, long2 )
		print "  Bearing: " + str(bearing) + " degrees"
	

# Call Main function - only for testing functions in this modules
#--------------------------------------------------------------------
if __name__ == "__main__":
	os.system("clear")
	print "--== Boat GPS Test Program ==--"
	main(sys.argv[1:])


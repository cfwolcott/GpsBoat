#!/usr/bin/python

# GPS Calc - January 2014

# Used to calculate distances between GPS locations

import time
import os
import sys
import math

PIER_LAT = 28.416
PIER_LONG = -80.593

STATION_41113_LAT = 28.400
STATION_41113_LONG = -80.530

# 20 mile buoy
STATION_41009_LAT = 28.523
STATION_41009_LONG = -80.184

#--------------------------------------------------------------------
# Returns distance from origin (lat1, lon1) to target location (lat2, lon2)
def CalcDistance( lat1, lon1, lat2, lon2 ):
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
def CalcBearing( lat1, lon1, lat2, lon2 ):
	dLon = math.radians(lon2 - lon1)
	lat1 = math.radians(lat1)
	lat2 = math.radians(lat2)
	
	y = math.sin(dLon) * math.cos(lat2)
	x = math.cos(lat1) * math.sin(lat2) \
		- math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
	theta = math.degrees( math.atan2(y, x) )
	return (theta + 360.0) % 360.0

#--------------------------------------------------------------------
def calcTurn(Btarget, Bcurrent):
	"""Returns tuple (turn angle [rads], turn dir [+1 == right, -1 == left])."""

	diff = Btarget - Bcurrent
	neg = diff < 0
	big = abs(diff) > PI

	if not neg and not big: theta = diff; lr = +1
	if not neg and big: theta = 2*PI - diff; lr = -1
	if neg and not big: theta = abs(diff); lr = -1
	if neg and big: theta = 2*PI - abs(diff); lr = +1

	return (theta, lr)
#--------------------------------------------------------------------
def main(argv):

	print "GPS Calc - Version 1.0"
	
	# Main loop
	while( True ):

		print "Distance from Peir to Buoy 41113 (close to shore)"
		target_bearing = CalcBearing( PIER_LAT, PIER_LONG, STATION_41113_LAT, STATION_41113_LONG )
		target_distance = CalcDistance( PIER_LAT, PIER_LONG, STATION_41113_LAT, STATION_41113_LONG )
		print "  Bearing:  " + str(target_bearing) + " degrees"
		if target_distance < 1.0:
			target_distance = target_distance * 5280
			print "  Distance: " + str(target_distance) + " feet"
		else:
			print "  Distance: " + str(target_distance) + " miles"

		print "Distance from Peir to 20 mile Buoy 41009"
		target_bearing = CalcBearing( PIER_LAT, PIER_LONG, STATION_41009_LAT, STATION_41009_LONG )
		target_distance = CalcDistance( PIER_LAT, PIER_LONG, STATION_41009_LAT, STATION_41009_LONG )
		print "  Bearing:  " + str(target_bearing) + " degrees"
		print "  Distance: " + str(target_distance) + " miles"

		exit()
		
#--------------------------------------------------------------------
if __name__ == "__main__":
	os.system("clear")
	print "--== Arduino Test Program ==--"
	main(sys.argv[1:])
	

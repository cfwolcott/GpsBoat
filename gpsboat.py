#!/usr/bin/python

# GPS Boat Project - January 2014

# This module is the main module that will be used to control all aspects of the boat

import time
import os
import sys
import math

import arduino

HOME_LAT = 33.879908
HOME_LONG = -117.947559

MARK_LAT = 28.58389
MARK_LONG = -80.809322

TEST_LAT = 33.879854
TEST_LONG = -117.950833

# System states for LED indicators
SYS_STATE_INIT = 1
SYS_STATE_WAITING_FOR_GPS_LOCK = 2
SYS_STATE_NAVIGATING = 3

# Arduino "defines" for rudder and motor registers
VERSION_REG = 0

STEERING_REG = 1
STEERING_NEUTRAL = 128
STEERING_LEFT = STEERING_NEUTRAL - 25
STEERING_RIGHT = STEERING_NEUTRAL + 25

MOTOR_REG = 2
MOTOR_OFF = 0
MOTOR_25 = 64
MOTOR_50 = 128
MOTOR_75 = 192
MOTOR_100 = 255

#--------------------------------------------------------------------
def SetSystemState( state ):

	if state == SYS_STATE_INIT:
		print "Initializing ..."
		
	elif state == SYS_STATE_WAITING_FOR_GPS_LOCK:
		print "Waiting for GPS lock ..."
		
	elif state == SYS_STATE_NAVIGATING:
		print "Ready for navigation"
		
	return

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

	print "GPS Boat - Version 1.0"
	
	# initialize system
	
	# arduino controller
	ard = arduino.Arduino()
	ard.SetI2cAddress( 0x4 )
	
	print "Ardweeny Version: " + str( ard.GetReg( VERSION_REG ) )

	print "Motor OFF"
	ard.SetReg( MOTOR_REG, MOTOR_OFF )
	
	print "Steering Servo Sequence ..."
	ard.SetReg( STEERING_REG, STEERING_LEFT )
	time.sleep(1)
	ard.SetReg( STEERING_REG, STEERING_NEUTRAL )
	time.sleep(1)
	ard.SetReg( STEERING_REG, STEERING_RIGHT )
	time.sleep(1)
	
	ard.SetReg( STEERING_REG, STEERING_NEUTRAL )
	
	# GPS
	
	# Main loop
	while( True ):

		# wait for GPS lock
		SetSystemState( SYS_STATE_INIT )

		SetSystemState( SYS_STATE_WAITING_FOR_GPS_LOCK )
						
		# begin navigation sequence
		SetSystemState( SYS_STATE_NAVIGATING )
		
		target_bearing = CalcBearing( HOME_LAT, HOME_LONG, MARK_LAT, MARK_LONG )
		target_distance = CalcDistance( HOME_LAT, HOME_LONG, MARK_LAT, MARK_LONG )
		print "Bearing:  " + str(target_bearing) + " degrees"
		print "Distance: " + str(target_distance) + " miles"
		
		target_bearing = CalcBearing( HOME_LAT, HOME_LONG, TEST_LAT, TEST_LONG )
		target_distance = CalcDistance( HOME_LAT, HOME_LONG, TEST_LAT, TEST_LONG )
		print "Bearing:  " + str(target_bearing) + " degrees"
		if target_distance < 1.0:
			target_distance = target_distance * 5280
			print "Distance: " + str(target_distance) + " feet"
		else:
			print "Distance: " + str(target_distance) + " miles"
		
		exit()
		
#--------------------------------------------------------------------
if __name__ == "__main__":
	os.system("clear")
	print "--== Arduino Test Program ==--"
	main(sys.argv[1:])
	

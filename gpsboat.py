#!/usr/bin/python

# GPS Boat Project - January 2014

# This module is the main module that will be used to control all aspects of the boat

import time
import os
import sys
import math

ENABLE_ARDWEENY = 0
#import arduino
import boatgps

PIER_LAT = 28.416
PIER_LONG = -80.593

STATION_41113_LAT = 28.400
STATION_41113_LONG = -80.530

# 20 mile buoy
STATION_41009_LAT = 28.523
STATION_41009_LONG = -80.184

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

	if ENABLE_ARDWEENY:
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
	g = boatgps.BoatGps()

	# Main loop
	while( True ):

		# wait for GPS lock
		SetSystemState( SYS_STATE_INIT )

		SetSystemState( SYS_STATE_WAITING_FOR_GPS_LOCK )
						
		# begin navigation sequence
		SetSystemState( SYS_STATE_NAVIGATING )
		
		print "Distance and Bear to 4-mile marker from Pier:"
		target_bearing = g.CalcBearing( PIER_LAT, PIER_LONG, STATION_41113_LAT, STATION_41113_LONG )
		target_distance = g.CalcDistance( PIER_LAT, PIER_LONG, STATION_41113_LAT, STATION_41113_LONG )
		print "   Distance: " + str(target_distance) + " miles"
		print "   Bearing:  " + str(target_bearing) + " degrees"
		print

		print "Distance and Bear to 20-mile marker from Pier:"
		target_bearing = g.CalcBearing( PIER_LAT, PIER_LONG, STATION_41009_LAT, STATION_41009_LONG )
		target_distance = g.CalcDistance( PIER_LAT, PIER_LONG, STATION_41009_LAT, STATION_41009_LONG )
		print "   Distance: " + str(target_distance) + " miles"
		print "   Bearing:  " + str(target_bearing) + " degrees"
		print
		
		exit()
		
#--------------------------------------------------------------------
if __name__ == "__main__":
	os.system("clear")
	print "--== GpsBoat Test Program ==--"
	main(sys.argv[1:])
	

#!/usr/bin/python

# GPS Boat Project - January 2014

# This module will provide an interface to the Arduino (Ardweeny)
# that controls the steering server and motor speed controller

import smbus
import time
import os
import sys

class Arduino:

	# -----------------------------
	def __init__(self):
		# smbus is for I2C bus
		# for RPI version 1, use "bus = smbus.SMBus(0)"
		self.bus = smbus.SMBus(1)
		self.MAX_REGS = 20
		
	# -----------------------------
	def SetI2cAddress( self, addr ):
		self.address = addr
		
	# -----------------------------
	def SetReg( self, reg, value):
	
		if reg < self.MAX_REGS:
			# write the register we want to write to
			reg = reg | 0x80
			self.bus.write_byte(self.address, reg)
			#time.sleep(0.05)
			self.bus.write_byte(self.address, value)
			return True
		else:
			return False

	# -----------------------------
	def GetReg( self, reg ):
	
		if reg < self.MAX_REGS:
			# write the register we want to read from
			self.bus.write_byte(self.address, reg)
			#time.sleep(0.05)
			# now read back the data
			number = self.bus.read_byte(self.address)
			return number
		else:
			return False


#--------------------------------------------------------------------
def main(argv):

	print "Arduino Test"
	
	a = Arduino()
	a.SetI2cAddress( 0x4 )
	
	for i in range(0, 9):
		val = a.GetReg(i)
		print "Reg[" + str(i) + "] = " + hex(val)
		
	# write a register
	print "Writing 1 to reg 3 ..."
	a.SetReg(3, 1)
	print "Read back: " + hex(a.GetReg(3))

	while True:
		reg = input("Enter register to read from; 1 - 9: ")
		if reg == 0:
		    exit()

		number = a.GetReg(reg-1)
		print "RxData[", reg, "] = ", hex(number)
		print
	

# Call Main function - only for testing functions in this modules
#--------------------------------------------------------------------
if __name__ == "__main__":
	os.system("clear")
	print "--== Arduino Test Program ==--"
	main(sys.argv[1:])

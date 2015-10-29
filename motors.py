import time
import RPi.GPIO as GPIO

class motors(pinpos, pinneg): # pinpos and pinneg are pins on which the terminals from the motor driver are connected on the Raspberry Pi
	
	# Constructor to set up the motor
	def __init__(self):	
		GPIO.setup(pinpos, GPIO.OUT)
		GPIO.setup(pinneg, GPIO.OUT)
	
	# The function that starts and stops the motor
	def drive(self, direction):
		if(direction == 1):
			GPIO.output(pinpos, True)
			GPIO.output(pinneg, False)
		else if(direction == -1):
			GPIO.output(pinneg, True)
			GPIO.output(pinpos, False)
		else if(direction == 0):
			GPIO.output(pinpos, False)
			GPIO.output(pinneg, False)
		else:
			return -1
	
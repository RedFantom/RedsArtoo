import time
import RPi.GPIO as GPIO

class motors: # pinpos and pinneg are pins on which the terminals from the motor driver are connected on the Raspberry Pi
	
	# Shared Values
	pinp = 0
	pinn = 0
	
	# Constructor to set up the motor
	def __init__(self, pinpos, pinneg):	
		GPIO.setup(pinpos, GPIO.OUT)
		GPIO.setup(pinneg, GPIO.OUT)
		pinp = pinpos
		pinn = pinneg
	
	# The function that starts and stops the motor
	def drive(self, direction):
		if(direction == 1):
			GPIO.output(pinp, True)
			GPIO.output(pinn, False)
		else if(direction == -1):
			GPIO.output(pinn, True)
			GPIO.output(pinp, False)
		else if(direction == 0):
			GPIO.output(pinp, False)
			GPIO.output(pinn, False)
		else:
			return -1
	

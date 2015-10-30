import time
import RPi.GPIO as GPIO

# The class for the lightsensors
class lightsensors:
	
	# Sharedvalues
	pin = 0	
	
	# The constructor to set up the necesssary GPIO pin
	def __init__(self, pin):
		GPIO.setup(pin, GPIO.IN)
		self.pin = pin

	# The function to call when  you want to know whether it's light or dark
	def light(self):
		return GPIO.input(self.pin)

# The class for the HC-SR04 distance sensors		
class distancesensor:
	
	# Shared Values
	pintrig = 0
	pinecho = 0

	# Set up the GPIO pins
	def __init__(self, pintrig, pinecho):
		GPIO.setup(pintrig, GPIO.OUT)
		GPIO.setup(pinecho, GPIO.IN)
		self.pintrig = pintrig
		self.pinecho = pinecho
	
	# The function that returns the approximate distance to an object
	def distance(self):
		GPIO.output(self.pintrig, True)
        	time.sleep(0.00001)
        	GPIO.output(self.pintrig, False)
        	while(GPIO.input(self.pinecho) == 0):
            		t_one = time.time()
        	while(GPIO.input(self.pinecho) == 1):
            		t_two = time.time()
        	deltat = t_two - t_one
        	return round(deltat * 17150, 0)

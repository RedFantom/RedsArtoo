import time
import RPi.GPIO as GPIO

# The class for the lightsensors
class lightsensors:
	
	# The constructor to set up the necesssary GPIO pin
	def __init__(self, pin):
		GPIO.setup(pin, GPIO.IN)
	
	gpiopin = pin
	# The function to call when  you want to know whether it's light or dark
	def light(self):
		return GPIO.input(gpiopin)

# The class for the HC-SR04 distance sensors		
class distancesensor:
	
	# Set up the GPIO pins
	def __init__(self, pintrig, pinecho):
		GPIO.setup(pintrig, GPIO.OUT)
		GPIO.setup(pinecho, GPIO.IN)
	
	pint = pintrig
	pine = pinecho
	
	# The function that returns the approximate distance to an object
	def distance(self):
		GPIO.output(pint, True)
        time.sleep(0.00001)
        GPIO.output(pint, False)
        while(GPIO.input(pine) == 0):
            t_one = time.time()
        while(GPIO.input(pine) == 1):
            t_two = time.time()
        deltat = t_two - t_one
        return round(deltat * 17150, 0)

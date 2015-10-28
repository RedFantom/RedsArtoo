import time
import RPi.GPIO as GPIO

# The class for the lightsensors
class lightsensors(pin):
	
	# The constructor to set up the necesssary GPIO pin
	def __init__(self):
		GPIO.setup(pin, GPIO.IN)
	
	# The function to call when  you want to know whether it's light or dark
	def light(self):
		return GPIO.input(pin)

# The class for the HC-SR04 distance sensors		
class distancesensor(pintrig, pinecho):
	
	# Set up the GPIO pins
	def __init__(self):
		GPIO.setup(pintrig, GPIO.OUT)
		GPIO.setup(pinecho, GPIO.IN)
	
	# The function that returns the approximate distance to an object
	def distance(self):
		GPIO.output(pintrig, True)
        time.sleep(0.00001)
        GPIO.output(pintrig, False)
        while(GPIO.input(pinecho) == 0):
            t_one = time.time()
        while(GPIO.input(pinecho) == 1):
            t_two = time.time()
        deltat = t_two - t_one
        return round(deltat * 17150, 0)

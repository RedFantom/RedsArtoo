import time
import RPi.GPIO as GPIO
import objects

# Class to control the spotlights in the holoprojectors of the droid
class spotlight:
    pin = 0

    # Set up the GPIO
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)

    # status is a boolean
    def setstate(self, status):
        GPIO.output(self.pin, status)

# Class to control the rgb led's in the sensors of the droid
class rgbled:
    pinred = 0
    pingreen = 0
    pinblue = 0

    # Contstructor sets up the GPIO
    def __init__(self, pinred, pingreen, pinblue):
        self.pinred = pinred
        self.pingreen = pingreen
        self.pinblue = pinblue

        GPIO.setup(pinred, GPIO.OUT)
        GPIO.setup(pingreen, GPIO.OUT)
        GPIO.setup(pinblue, GPIO.OUT)

    # Red, green and blue are booleans
    def setstate(self, red, green, blue):
        GPIO.output(self.pinred, red)
        GPIO.output(self.pingreen, green)
        GPIO.output(self.pinblue, blue)

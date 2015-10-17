import time
import functions
import gpgpio as GPIO

OUT = "output"
IN = "input"
BCM = "BCM"
PUD_UP = "high voltage"
PUD_DOWN = "low voltage"

def motorright(direction):
    if(direction == 0):
        GPIO.output(23, False)
        GPIO.output(24, False)
    if(direction == 1):
        GPIO.output(23, False)
        GPIO.output(24, False)
        GPIO.output(23, True)
    if(direction == -1):
        GPIO.output(23, False)
        GPIO.output(24, False)
        GPIO.output(24, True)

def motorleft(direction):
    if(direction == 0):
        GPIO.output(25, False)
        GPIO.output(26, False)
    if(direction == 1):
        GPIO.output(25, False)
        GPIO.output(26, False)
        GPIO.output(25, True)
    if(direction == -1):
        GPIO.output(25, False)
        GPIO.output(26, False)
        GPIO.output(26, True)

def motordome(direction):
    if(direction == 0):
        GPIO.output(27, False)
        GPIO.output(28, False)
    if(direction == 1):
        GPIO.output(27, False)
        GPIO.output(28, False)
        GPIO.output(27, True)
    if(direction == -1):
        GPIO.output(27, False)
        GPIO.output(28, False)
        GPIO.output(28, True)

def rgb(red, green, blue):


def holoprojectors(lights):

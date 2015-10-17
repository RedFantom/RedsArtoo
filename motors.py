import GPIO
import functions
import time

# These are variables to be used by the whole file
dometurned = 0

# I haven't actually built the droid yet, so these are just example values
bodyconstant = 0.01
domeconstant = 0.01

def drive(direction):
    if(direction == "forward"):
        GPIO.motorleft(1)
        GPIO.motorright(1)
    if(direction == "backward"):
        GPIO.motorleft(-1)
        GPIO.motorright(-1)

def turn(part, degrees):
    if(part == "body"):
        if(degrees > 0):
            GPIO.motorleft(1)
            GPIO.motorright(-1)
            time.wait(degrees * bodyconstant)
            stop("body")
        if(degrees < 0):
            GPIO.motorright(1)
            GPIO.motorleft(-1)
            time.wait(degrees * bodyconstant)
            stop("body")
    if(part == "dome"):
        if(degrees > 0):
            GPIO.motordome(1)
            time.wait(degrees * domeconstant)
            stop("dome")
        if(degrees < 0):
            GPIO.motordome(-1)
            time.wait(degrees * domeconstant)
            stop("dome")

def stop(motors):
    if(motors == "all"):
        GPIO.motordome(0)
        GPIO.motorright(0)
        GPIO.motorleft(0)
    if(motors == "dome"):
        GPIO.motordome(0)
    if(motors == "body"):
        GPIO.motorleft(0)
        GPIO.motorright(0)

import motors
import time

leftmotor = motors.motors(1, 2)
rightmotor = motors.motors(3, 4)
domemotor = motors.motors(5, 6)
dometurned = 0

# Function to drive the droid
def drive(direction):
    if(direction == "none"):
        leftmotor.setstate(0)
        rightmotor.setstate(0)
    if(direction == "left"):
        leftmotor.setstate(1)
        rightmotor.setstate(-1)
    if(direction == "right"):
        leftmotor.setstate(-1)
        rightmotor.setstate(1)
    if(direction == "forward"):
        leftmotor.setstate(1)
        rightmotor.setstate(1)
    if(direction == "backward"):
        leftmotor.setstate(-1)
        rightmotor.setstate(-1)

# Function to turn the dome of the droid
def turndome(degrees):

    # < 0 turns the dome
    if(degrees < 0):
        dometurned = dometurned + degrees
        domemotor.setstate(-1)
        time.sleep((degrees * -1) / 360)
        domemotor.setstate(0)

    # 0 resets the dome to its default position
    else if(degrees == 0):
        if(dometurned < 0):
            domemotor.setstate(1)
            time.sleep((dometurned * -1) / 360)
            domemotor.setstate(0)
            dometurned = 0
        if(dometurned > 0):
            domemotor.setstate(-1)
            time.sleep(dometurned / 360)
            domemotor.setstate(0)
            dometurned = 0
            
    # > 0 turns the dome
    else if(degrees > 0):
        dometurned = dometurned + degrees
        domemotor.setstate(1)
        time.sleep(degrees / 360)
        domemotor.setstate(0)
        dometurned = dometurned + degrees

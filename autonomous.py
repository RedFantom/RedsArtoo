import drive
import lights
import sensors
import XboxController
import objects
import multiprocessing
import accelerometer
import time
import RPi.GPIO as GPIO
from i2clibraries import i2c_hmc5883l

# The planning as of 02-12-2015 for the autonomous file is:

# As for the motors:

# Directions with travel of 25 cm or less are inaccessible
# Directions are measured in degrees from the working line of the forward direction
# 1. Determine of all possible travelling directions
#   - Determine the direction of the sound (if there is none, this is blank)
#   - Determine the distances to objects around the droid
#     * Steps of 5 or 10 degrees
#     * A distance of 100 cm to an object or more is acceptable
# 2. Decide what direction to go in
#   - XboxController OVERRULES all other directions if XboxController presents a direction
#   - The direction of the sound has priority
#     * If it is not directly accessible, choose the direction that requires the smallest turn, but only if the travel distance is more than 50 cm
#     * If it is directly accessible, but does not allow for more than 50 cm of travel, continue as if it were inaccessible
#     * If there is no option with more than 50 cm of travel distance, continue as if there was no sound
#   - If there is no sound, the direction in which we can travel furthest has priority, as long as it doesn't make for a turn of 90 degrees or more
#   - The direction which the droid just came from, and thus a turn of 180 degrees, has the lowest priority
#   - If objects in all directions are just as far away, go forward
#   - If forward is not an option, preferably do not strain more than 90 degrees of course
# 3. Move in the direction and keep updating the distance and sound information
#   - This means that the dome has to be turning continously while driving
#   - If the accelerometer detects no movement, but the Leg motors are both on for half a second: halt immediately
#     * If the accelerometer does not detect movement, but the motors are on, the motors, drivers or distance sensors might be faulty, but more importantly, it could cause a very large current to be drawn from the motor drives and thus the battery, which might break even more.
# 4. Start from step one while still driving

# As for the Bright LEDs
# 1. Check for each of the sensors whether or not it is "dark"
# 2. For each of the "dark" sensors, set the Bright LED to on
# 3. Wait half a minute, then turn the LEDs off

# As for the Sensors:
# % of directions| >50% | 50% with 10% margin | <50%
# ---------------|------|---------------------|------
# colour of front| Blue |       Purple        | Red
#
# Sound direction| True | False
# ---------------|------|--------
# colour of back | Green| Yellow

BatteryLow = False
Distances = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
DirectionAccessability = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,]
SoundDirection = 0
SoundDirectionPresent = False
CompassHeadingDegrees = 0
CompassHeadingMinutes = 0       # This really confused me at first, but apparently minutes are one-sixtieth of a degree
xRotation = 0
yRotation = 0
ShutdownRequested = False
CurrentDirection = 0
ChosenDirection = 0
# This function is written in the assumption that the dome turns at 60RPM at full speed
def distances():
    while True:
        # The ShutdownRequested needs to be checked multiple times, because the whole function takes a lot of time to complete.
        # The function is only stopped when the dome is in a normal position
        if(ShutdownRequested == True):
            break

        # Declaring variables
        TimeTurned = 0.00
        DegreesTurned = 0.0
        # The Distance sensors will not be looking straight forward and backward, so these values will be changed in time.
        DistancePositionOne = 0
        DistancePositionTwo = 20

        # Here the dome gets turning. The pwm function from takes 0.02 seconds, so the code should be executed fifty times
        while(TimeTurned <= 1.00):
            # Turn the dome and record the degrees turned
            objects.MotorDome.pwm(1, 0.25)
            DegreesTurned = DegreesTurned + 1.8
            # Every 9.0 degrees the distances from the distance sensors in the dome needs to be recorded.
            if(DegreesTurned % 9.0 == 0.0):
                Distances[DistancePositionOne] = objects.DistanceOne.distance()
                Distances[DistancePositionTwo] = objects.DistanceTwo.distance()
                DistancePositionOne = DistancePositionOne + 1
                DistancePositionTwo = DistancePositionTwo + 1
            # Record the time turned so the function quits after 50 times
            TimeTurned = TimeTurned + 0.02
        # Reset the TimeTurned to be ready for the second quarter turn.
        TimeTurned = 0.0
        DegreesTurned = 0.0
        # Turn the dome back. The distances are not measured again. I might change this in the future if necessary.
        while(TimeTurned <= 1.00):
            objects.MotorDome.pwm(-1, 0.25)
            TimeTurned = TimeTurned + 0.02
        TimeTurned = 0
        # Check the ShutdownRequested again, the dome is in normal position
        if(ShutdownRequested == True):
            break
        # Do the same thing as before, but now in the opposite direction.
        while(TimeTurned <= 1.00):
            objects.MotorDome.pwm(-1, 0.25)
            DegreesTurned = DegreesTurned + 1.8
            if(DegreesTurned % 9.0 == 0.0):
                Distances[DistancePositionOne] = objects.DistanceOne.distance()
                Distances[DistancePositionTwo] = objects.DistanceTwo.distance()
                DistancePositionOne = DistancePositionOne + 1
                DistancePositionTwo = DistancePositionTwo + 1
            TimeTurned = Timeturned + 0.02
        # Reset the TimeTurned
        TimeTurned = 0
        # Turn the dome back again to normal position
        while(TimeTurned <= 1.00):
            objects.MotorDome.pwm(1, 0.25)
            TimeTurned = TimeTurned + 0.02
        # Check the ShutdownRequested again.
        if(ShutdownRequested == True):
            break

def ShutdownRequester():
    # ShutdownRequester function to check the whether the shutdown switch is turned on
    GPIO.setup(objects.ShutdownSwitch, GPIO.IN)
    GPIO.setup(objects.BatterySensor, GPIO.IN)
    while(ShutdownRequested == False):
        if(GPIO.input(objects.ShutdownSwitch) == 1):
            # If the shutdown switch is pressed, set the ShutDownRequested to True
            ShutdownRequested = True
            break
        if(GPIO.input(BatterySensor) == 0):
            BatteryLow = True

def compass():
    # Create an object for the electronic compass, should be moved to the objects file
    compass = i2c_hmc5883l.i2c_hmc5883l(1)
    # Set the compass to measure continuously
    compass.setContinuousMode()
    # This is where it gets tricky. The setDeclination function is to set the magnetic declination for the place you want to use the compass
    # For The Netherlands the magnetic Declination is 0,5 degrees per 7 radialdegrees
    compass.setDeclination(0.5, 7)
    while(True):
        # Break when a shutdown is requested
        if(ShutdownRequested == True):
            break
        # Else update the heading variables of the droid
        else:
            (CompassHeadingDegrees, CompassHeadingMinutes) = compass.getHeading()

def Accelerometer():
    while True:
        if(ShutDownRequested == True):
            Break
        else:
            (xRotation, yRotation) = accelerometer.update()

def sound():
    while True:
        if(ShutdownRequested == True):
            break
        else:
            while(objects.SoundSensorOne.sound() == True or objects.SoundSensorTwo.sound == True or objects.SoundSensorThree.sound() == True):
                if(ShutdownRequested == True):
                    break
            while(objects.SoundSensorOne.sound() == False and objects.SoundSensorTwo.sound() == False and objects.SoundSensorThree() == False):
                if(ShutdownRequested == True):
                    break
            while True:
                SensorOneDetected = False
                SensorTwoDetected = False
                SensorThreeDetected = False
                if(objects.SoundSensorOne.sound() == True and SoundOneDetected == False):
                    SensorOneTime = time.time()
                if(objects.SoundSensorTwo.sound() == True and SoundTwoDetected == False):
                    SensorTwoTime = time.time()
                if(objects.SoundSensorThree.sound() == True and SoundThreeDetected == False):
                    SensorThreeTime = time.time()
                if(SensorOneDetected == True and SensorTwoDetected == True and SensorThreeDetected == True):
                    break
            if(SensorOneTime < SensorTwoTime and SensorOneTime < SensorThreeTime):
                SoundDirectionPresent = True
                SoundDirection = 0
            elif(SensorTwoTime < SensorOneTime and SensorTwoTime < SensorThreeTime):
                SoundDirectionPresent = True
                SoundDirection = 12
            elif(SensorThreeTime < SensorOneTime and SensorThreeTimee < SensorTwoTime):
                SoundDirectionPresent = True
                SoundDirection = 26
            else:
                SoundDirectionPresent = False
                raise ValueError('SoundDirection not present')

def main():
    DistanceProcess = multiprocessing.Process(target = distance)
    ShutdownRequesterProcess = multiprocessing.Process(target = ShutdownRequester)
    CompassProcess = multiprocessing.Process(target = compass)
    AccelerometerProcess = multiprocessing.Process(target = Accelerometer)
    while True:
        if(ShutdownRequested == True):
            break
        DistanceNumber = 0
        for distance in Distances:
            if(distance <= 50 and distance > 0):
                DirectionAccessability[DistanceNumber] == False
            elif(distance > 50):
                DirectionAccessability[DistanceNumber] == True
            elif(distance <= 0):
                raise ValueError 'A Distance smaller than or equal to Zero'
        if(SoundDirectionPresent == True):
            if(DirectionAccessability[SoundDirection] == True and DirectionAccessability[SoundDirection + 1] == True and DirectionAccessability[SoundDirection - 1] == True):
                if(SoundDirection == 0):
                    ChosenDirection = 0
                elif(SoundDirection == 12):
                    ChosenDirection = 120
                elif(SoundDirection == 26):
                    ChosenDirection = 240
            elif(DirectionAccessability[SoundDirection] == False):
                if(DirectionAccessability[SoundDirection + 1] == True and DirectionAccessability[SoundDirection + 2] == True and DirectionAccessability[SoundDirection + 3] == True):
                    ChosenDirection = (SoundDirection + 2) * 9
                elif(DirectionAccessability[SoundDirection - 1] == True and DirectionAccessability[SoundDirection - 2] == True and DirectionAccessability[SoundDirection - 3] == True):
                    ChosenDirection = (SoundDirection - 2) * 9
                elif(DirectionAccessability[SoundDirection + 2] == True and DirectionAccessability[SoundDirection + 3] == True and DirectionAccessability[SoundDirection + 4] == True):
                    ChosenDirection = (SoundDirection + 3) * 9
                elif(DirectionAccessability[SoundDirection - 2] == True and DirectionAccessability[SoundDirection - 3] == True and DirectionAccessability[SoundDirection - 4] == True):
                    ChosenDirection = (SoundDirection - 3) * 9
                else:
                    AccessibleNumber = 0
                    for Accessible in DirectionAccessability:
                        if(Accessible = True and DirectionAccessability[AccessibleNumber + 1] == True and DirectionAccessability[AccessibleNumber + 2] == True):
                            ChosenDirection = AccessibleNumber * 9
                            break
                        elif(DirectionAccessability[-AccessibleNumber] == True and DirectionAccessability[-AccessibleNumber - 1] == True and DirectionAccessability[-AccessibleNumber - 2] == True):
                            ChosenDirection = 360 - (AccessibleNumber * 9)
                            break
                        else:
                            AccessibleNumber = AccessibleNumber + 1
        else:
            AccessibleNumber = 0
            for Accessible in DirectionAccessability:
                if(Accessible = True and DirectionAccessability[AccessibleNumber + 1] == True and DirectionAccessability[AccessibleNumber + 2] == True):
                    ChosenDirection = AccessibleNumber * 9
                    break
                elif(DirectionAccessability[-AccessibleNumber] == True and DirectionAccessability[-AccessibleNumber - 1] == True and DirectionAccessability[-AccessibleNumber - 2] == True):
                    ChosenDirection = 360 - (AccessibleNumber * 9)
                    break
                else:
                    AccessibleNumber = AccessibleNumber + 1

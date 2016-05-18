import motors
import lights
import sensors
import XboxController
import multiprocessing
import accelerometer
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_NeoPixel
from i2clibraries import i2c_hmc5883l
from objects import *

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
# % of directions| >60% | 40-60% | <40%
# ---------------|------|--------|------
# colour of front| Blue | Purple | Red
#
# Sound direction| True | False
# ---------------|------|--------
# colour of back | Green| Yellow

BatteryLow = False
Distances = [0] * 40
DirectionAccessability = [False] * 40
SoundDirection = 0
SoundDirectionPresent = False
CompassHeadingDegrees = 0
CompassHeadingMinutes = 0       # This really confused me at first, but apparently minutes are one-sixtieth of a degree
xRotation = 0
yRotation = 0
ShutdownRequested = False
CurrentDirection = 0
ChosenDirection = 0
TurnNeeded = False
indexLights = 0

# This function is written in the assumption that the dome turns at 60RPM at full speed
def distances():
    while True:
        # The ShutdownRequested needs to be checked multiple times, because the whole function takes a lot of time to complete.
        # The function is only stopped when the dome is in a normal position
        if ShutdownRequested:
            break

        # Declaring variables
        TimeTurned = 0.00
        DegreesTurned = 0.0
        # The Distance sensors will not be looking straight forward and backward, so these values will be changed in time.
        DistancePositionOne = 0
        DistancePositionTwo = 20

        # Here the dome gets turning. The pwm function from takes 0.02 seconds, so the code should be executed fifty times
        while TimeTurned <= 1.00:
            # Turn the dome and record the degrees turned
            objects.MotorDome.pwm(1, 0.25)
            DegreesTurned = DegreesTurned + 1.8
            # Every 9.0 degrees the distances from the distance sensors in the dome needs to be recorded.
            if DegreesTurned % 9.0 == 0.0:
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
        while TimeTurned <= 1.00:
            objects.MotorDome.pwm(-1, 0.25)
            TimeTurned = TimeTurned + 0.02
        TimeTurned = 0
        # Check the ShutdownRequested again, the dome is in normal position
        if ShutdownRequested:
            break
        # Do the same thing as before, but now in the opposite direction.
        while TimeTurned <= 1.00:
            objects.MotorDome.pwm(-1, 0.25)
            DegreesTurned = DegreesTurned + 1.8
            if DegreesTurned % 9.0 == 0.0:
                Distances[DistancePositionOne] = objects.DistanceOne.distance()
                Distances[DistancePositionTwo] = objects.DistanceTwo.distance()
                DistancePositionOne = DistancePositionOne + 1
                DistancePositionTwo = DistancePositionTwo + 1
            TimeTurned = Timeturned + 0.02
        # Reset the TimeTurned
        TimeTurned = 0
        # Turn the dome back again to normal position
        while TimeTurned <= 1.00:
            objects.MotorDome.pwm(1, 0.25)
            TimeTurned = TimeTurned + 0.02
        # Check the ShutdownRequested again.
        if ShutdownRequested:
            break

def ShutdownRequester():
    # ShutdownRequester function to check the whether the shutdown switch is turned on
    GPIO.setup(objects.ShutdownSwitch, GPIO.IN)
    GPIO.setup(objects.BatterySensor, GPIO.IN)
    while not ShutdownRequested:
        if GPIO.input(objects.ShutdownSwitch) == 1:
            # If the shutdown switch is pressed, set the ShutDownRequested to True
            ShutdownRequested = True
            break
        if GPIO.input(BatterySensor) == 0:
            BatteryLow = True


def compass():
    # Create an object for the electronic compass, should be moved to the objects file
    compass = i2c_hmc5883l.i2c_hmc5883l(1)
    # Set the compass to measure continuously
    compass.setContinuousMode()
    # This is where it gets tricky. The setDeclination function is to set the magnetic declination for the place you want to use the compass
    # For The Netherlands the magnetic Declination is 0,5 degrees per 7 radialdegrees
    compass.setDeclination(0.5, 7)
    while True:
        # Break when a shutdown is requested
        if ShutdownRequested:
            break
        # Else update the heading variables of the droid
        else:
            (CompassHeadingDegrees, CompassHeadingMinutes) = compass.getHeading()

def Accelerometer():
    while True:
        if ShutDownRequested:
            Break
        else:
            (xRotation, yRotation) = accelerometer.update()

def sound():
    while True:
        if ShutdownRequested:
            break
        else:
            while objects.SoundSensorOne.sound() or objects.SoundSensorTwo.sound() or objects.SoundSensorThree.sound():
                if ShutdownRequested:
                    break
            while not objects.SoundSensorOne.sound() and not objects.SoundSensorTwo.sound() and not objects.SoundSensorThree():
                if ShutdownRequested:
                    break
            while True:
                SensorOneDetected = False
                SensorTwoDetected = False
                SensorThreeDetected = False
                if objects.SoundSensorOne.sound() and not SoundOneDetected:
                    SensorOneTime = time.time()
                if objects.SoundSensorTwo.sound() and not SoundTwoDetected:
                    SensorTwoTime = time.time()
                if objects.SoundSensorThree.sound() and not SoundThreeDetected:
                    SensorThreeTime = time.time()
                if SensorOneDetected and SensorTwoDetected and SensorThreeDetected:
                    break
            if SensorOneTime < SensorTwoTime and SensorOneTime < SensorThreeTime:
                SoundDirectionPresent = True
                SoundDirection = 0
            elif SensorTwoTime < SensorOneTime and SensorTwoTime < SensorThreeTime:
                SoundDirectionPresent = True
                SoundDirection = 12
            elif SensorThreeTime < SensorOneTime and SensorThreeTime < SensorTwoTime:
                SoundDirectionPresent = True
                SoundDirection = 26
            else:
                SoundDirectionPresent = False
                raise ValueError('SoundDirection not present')

def lights():
    SensorOne.begin()
    SensorTwo.begin()
    SensorOneCurrentState = "none"
    SensorTwoCurrentState = "none"
    SpotLightOneCurrentState = 0
    SpotLightTwoCurrentState = 0
    indexLights = 0
    while True:
        if ShutdownRequested:
            break
        if SoundDirectionPresent:
            if SensorTwoCurrentState == "none":
                indexLights = 0
                while indexLights < SensorAmountOfLeds:
                    SensorTwo.setPixelColor(indexLights, 0, 255, 0)
                    indexLights = indexLights + 1
                SensorTwo.show()
                SensorOneCurrentState = "green"
            elif SensorTwoCurrentState == "green":
                while indexLights < SensorAmountOfLeds:
                    SensorTwo.setPixelColor(indexLights, 0, 255, 0)
                    indexLights = indexLights + 1
                SensorTwo.show()
                SensorTwoCurrentState = "green"
            elif SensorTwoCurrentState == "yellow":
                intensity = 255
                while intensity > -1:
                    indexLights = 0
                    while indexLights < SensorAmountOfLeds:
                        SensorTwo.setPixelColor(indexLights, intensity, 255, 0)
                        indexLights = indexLights + 1
                    SensorTwo.show()
                    intensity = intensity - 1
                    time.sleep(0.005)
            else:
                raise ValueError('SensorTwoCurrentState is neither none nor green nor yellow')
        if not SoundDirectionPresent:
            if SensorTwoCurrentState == "none":
                indexLights = 0
                while indexLights < SensorAmountOfLeds:
                    SensorTwo.setPixelColor(indexLights, 255, 255, 0)
                    indexLights = indexLights + 1
                SensorTwo.show()
                SensorTwoCurrentState == "yellow"
            elif SensorTwoCurrentState == "green":
                intensity = 0
                while intensity < 256:
                    indexLights = 0
                    while indexLights < SensorAmountOfLeds:
                        SensorTwo.setPixelColor(indexLights, intensity, 255, 0)
                        indexLights = indexLights + 1
                    SensorTwo.show()
                    intensity = intensity + 1
                    time.sleep(0.005)
                SensorTwoCurrentState = "yellow"
            elif SensorTwoCurrentState == "yellow":
                indexLights = 0
                while indexLights < SensorAmountOfLeds:
                    SensorTwo.setPixelColor(indexLights, 255, 255, 0)
                    indexLights = indexLights + 1
                SensorTwo.show()
                SensorTwoCurrentState = "yellow"
            else:
                raise ValueError('SensorTwoCurrentState is neither none nor green nor yellow')
        if ShutdownRequested:
            break
        DirectionAccessabilityPercentage = 0
        AccessibleCount = 0
        for accessible in DirectionAccessability:
            if accessible:
                AccessibleCount = AccessibleCount + 1
        DirectionAccessabilityPercentage = (AccessibleCount / 40) * 100
        if DirectionAccessability < 40:
            if SensorOneCurrentState == "none":
                indexLights = 0
                while indexLights < SensorAmountOfLeds:
                    indexLights = indexLights + 1
                    SensorOne.setPixelColor(indexLights, 255, 0, 0)
                SensorOne.show()
                SensorOneCurrentState = "red"
            elif SensorOneCurrentState == "red":
                indexLights = 0
                while indexLights < SensorAmountOfLeds:
                    SensorOne.setPixelColor(indexLights, 255, 0, 0)
                    indexLights = indexLights + 1
                SensorOne.show()
                SensorOneCurrentState = "red"
            elif SensorOneCurrentState == "blue":
                intensityOne = 0
                intensityTwo = 255
                while intensityOne < 256:
                    indexLights = 0
                    while indexLights < SensorAmountOfLeds:
                        SensorOne.setPixelColor(indexLights, intensityOne, 0, intensityTwo)
                        indexLights = indexLights + 1
                    SensorOne.show()
                    intensityOne = intensityOne + 1
                    time.sleep(0.05)
                SensorOneCurrentState = "red"
            elif SensorOneCurrentState == "purple":
                intensityOne = 255
                while intesityOne > -1:
                    indexLights = 0
                    while indexLights < SensorAmountOfLeds:
                        SensorOne.setPixelColor(indexLights, 255, 0, intensityOne)
                        indexLights = indexLights + 1
                    intensityOne = intensityOne - 1
                    SensorOne.show()
                    time.sleep(0.05)
                SensorOneCurrentState = "red"
            else:
                raise ValueError('The SensorOneCurrentState is neither none nor red nor blue nor purple')
        elif DirectionAccessabilityPercentage >= 40 and DirectionAccessabilityPercentage <= 60:
            if SensorOneCurrentState == "blue":
                intensityOne = 0
                while intensityOne < 255:
                    indexLights = 0
                    while indexLights < SensorAmountOfLeds:
                        SensorOne.setPixelColor(indexLights, intensityOne, 0, 255)
                        indexLights = indexLights + 1
                    intensityOne = intensityOne + 1
                    SensorOne.show()
                    time.sleep(0.05)
                SensorOneCurrentState = "purple"
            elif SensorOneCurrentState == "purple" or SensorOneCurrentState == "none":
                indexLights = 0
                while indexLights < SensorAmountOfLeds:
                    SensorOne.setPixelColor(indexLights, 255, 0, 255)
                    indexLights = indexLights + 1
                SensorOne.show()
                SensorOneCurrentState = "purple"
            elif SensorOneCurrentState == "red":
                intensityOne = 0
                while intensityOne < 256:
                    indexLights = 0
                    while indexLights < SensorAmountOfLeds:
                        SensorOne.setPixelColor(indexLights, 255, 0, intensityOne)
                        indexLights = indexLights + 1
                    intensityOne = intensityOne + 1
                    SensorOne.show()
                    time.sleep(0.05)
                SensorOneCurrentState = "purple"
            else:
                raise ValueError('The SensorOneCurrentState is neither none nor red nor blue nor purple')
        elif DirectionAccessabilityPercentage > 60:
            if SensorOneCurrentState == "red":
                intensityOne = 0
                intensityTwo = 255
                while intensityOne < 256:
                    indexLights = 0
                    while indexLights < SensorAmountOfLeds:
                        SensorOne.setPixelColor(indexLights, intensityOne, 0, intensityTwo)
                        indexLights = indexLights + 1
                    intensityOne = intensityOne + 1
                    intensityTwo = intensityTwo - 1
                    SensorOne.show()
                    time.sleep(0.05)
                SensorOneCurrentState = "blue"
            elif SensorOneCurrentState == "purple":
                intensityOne = 0
                while intensityOne > -1:
                    indexLights = 0
                    while indexLights < SensorAmountOfLeds:
                        SensorOne.setPixelColor(indexLights, intensityOne, 0, 255)
                        indexLights = indexLights + 1
                    intensityOne = intensityOne - 1
                    SensorOne.show()
                    time.sleep(0.05)
                SensorOneCurrentState = "blue"
            elif SensorOneCurrentState == "blue" or SensorOneCurrentState == "none":
                indexLights = 0
                while indexLights < SensorAmountOfLeds:
                    SensorOne.setPixelColor(indexLights, 0, 0, 255)
                    indexLights = indexLights + 1
                SensorOne.show()
                SensorOneCurrentState = "blue"
            else:
                raise ValueError('The SensorOneCurrentState is neither none nor red nor blue nor purple')
        else:
            raise ValueError('The DirectionAccessabilityPercentage is a complex number, or non-existent')


# Work to do comes here

def drive():
    DistanceProcess.start()
    ShutdownRequesterProcess.start()
    CompassProcess.start()
    AccelerometerProcess.start()
    while True:
        if ShutdownRequested:
            break
        DistanceNumber = 0
        for distance in Distances:
            if distance <= 50 and distance > 0:
                DirectionAccessability[DistanceNumber] = False
            elif distance > 50:
                DirectionAccessability[DistanceNumber] = True
            elif distance <= 0:
                raise ValueError ('A Distance smaller than or equal to Zero')
        if SoundDirectionPresent:
            if DirectionAccessability[SoundDirection] and DirectionAccessability[SoundDirection + 1] and DirectionAccessability[SoundDirection - 1]:
                if SoundDirection == 0:
                    ChosenDirection = 0
                elif SoundDirection == 12:
                    ChosenDirection = 120
                elif SoundDirection == 26:
                    ChosenDirection = 240
            elif not DirectionAccessability[SoundDirection]:
                if DirectionAccessability[SoundDirection + 1]  and DirectionAccessability[SoundDirection + 2] and DirectionAccessability[SoundDirection + 3]:
                    ChosenDirection = (SoundDirection + 2) * 9
                elif DirectionAccessability[SoundDirection - 1] and DirectionAccessability[SoundDirection - 2] and DirectionAccessability[SoundDirection - 3]:
                    ChosenDirection = (SoundDirection - 2) * 9
                elif DirectionAccessability[SoundDirection + 2] and DirectionAccessability[SoundDirection + 3] and DirectionAccessability[SoundDirection + 4]:
                    ChosenDirection = (SoundDirection + 3) * 9
                elif DirectionAccessability[SoundDirection - 2] and DirectionAccessability[SoundDirection - 3] and DirectionAccessability[SoundDirection - 4]:
                    ChosenDirection = (SoundDirection - 3) * 9
                else:
                    AccessibleNumber = 0
                    for Accessible in DirectionAccessability:
                        if Accessible and DirectionAccessability[AccessibleNumber + 1] and DirectionAccessability[AccessibleNumber + 2]:
                            ChosenDirection = AccessibleNumber * 9
                            break
                        elif DirectionAccessability[-AccessibleNumber] and DirectionAccessability[-AccessibleNumber - 1] and DirectionAccessability[-AccessibleNumber - 2]:
                            ChosenDirection = 360 - (AccessibleNumber * 9)
                            break
                        else:
                            AccessibleNumber = AccessibleNumber + 1
        else:
            AccessibleNumber = 0
            for Accessible in DirectionAccessAbility:
                if Accessible and DirectionAccessAbility[AccessibleNumber + 1] and DirectionAccessAbility[AccessibleNumber + 2]:
                    ChosenDirection = Accessible * 9
                    break
                elif DirectionAccessability[-AccessibleNumber] and DirectionAccessability[-AccessibleNumber - 1] and DirectionAccessability[-AccessibleNumber - 2]:
                    ChosenDirection = Accessible * 9
                    break
                else:
                    AccessibleNumber = AccessibleNumber + 1

        if ChosenDirection > 360:
            raise ValueError('A direction larger than 360 degrees was chosen')
        if ChosenDirection > 180:
            ChosenDirection = (ChosenDirection - 180) * -1
        elif ChosenDirection < -180:
            ChosenDirection = (ChosenDirection + 180) * -1
        if ChosenDirection == 0:
            TurnNeeded = False
        else:
            TurnNeeded = True

        CurrentDirection = CompassHeadingDegrees
        NewDirection = CurrentDirection + ChosenDirection

        if NewDirection < 0:
            NewDirection = NewDirection * -1 + 180
        elif NewDirection > 360:
            NewDirection = NewDirection - 360
        elif NewDirection == 360:
            NewDirection = 0

        if not TurnNeeded:
            if ShutDownRequested:
                break
            objects.MotorLeft.setstate(1)
            objects.MotorRight.setstate(1)
            time.sleep(0.5)
            objects.MotorLeft.setstate(0)
            objects.MotorRight.setstate(0)
        if TurnNeeded:
            if ShutDownRequested:
                break
            if ChosenDirection < 0:
                objects.MotorLeft.setstate(1)
                while CompassHeadingDegrees != NewDirection:
                    time.sleep(0.001)
                objects.MotorLeft.setstate(0)
            elif ChosenDirection == 0:
                raise ValueError('No turn needed while TurnNeeded is True')
            elif ChosenDirection > 0:
                objects.MotorRight.setstate(1)
                while CompassHeadingDegrees != NewDirection:
                    time.sleep(0.001)
                objects.MotorRight.setstate(0)
        if ShutDownRequested:
            break

def ShutDown():
    GPIO.cleanup()
    if DistanceProcess.is_alive() or ShutdownRequesterProcess.is_alive() or CompassProcess.is_alive() or AccelerometerProcess.is_alive():
        time.sleep(5)
        DistanceAlive = DistanceProcess.is_alive()
        ShutdownReqAlive = ShutDownRequesterProcess.is_alive()
        CompassAlive = CompassProcess.is_alive()
        AccelAlive = AccelerometerProcess.is_alive()
        if DistanceAlive:
            DistanceProcess.terminate()
        if ShutDownReqAlive:
            ShutDownRequesterProcess.terminate()
        if CompassAlive:
            CompassProcess.terminate()
        if AccelAlive:
            AccelerometerProcess.terminate()
    sys.exit()

drive()

import drive
import lights
import sensors
import XboxController
import objects
import thread

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
# colour of front| Blue | Purple              | Red
#
# Sound direction| True | False
# ---------------|------|--------
# colour of back | Green| Yellow

BatteryLow = False
Distances = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# This function is written in the assumption that the dome turns at 60RPM at full speed
def distances():
    while(BatteryLow == False):
        TimeTurned = 0.00
        DegreesTurned = 0.0
        DistancePositionOne = 0
        DistancePositionTwo = 20
        while(TimeTurned <= 1.00):
            objects.MotorDome.pwm(1, 0.25)
            DegreesTurned = DegreesTurned + 1.8
            if(DegreesTurned % 9 == 0):
                Distances[DistancePositionOne] = objects.DistanceOne.distance()
                Distances[DistancePositionTwo] = objects.DistanceOne.distance()

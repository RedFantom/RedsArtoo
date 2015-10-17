import time
import motors
import sensors
import lights
import sound
import camera
import matrix
import remotecontrol
import GPIO
import system from os as terminal


def autonomous():

    while True:

        # Check if there are any objects blocking the way of the droid
		if(sensors.distance("body") <= 50):

		# If yes, start actions to avoid the object
			motors.stop("all")
			dometurned = 0
			safedistance = False
			while(sensors.distance("dome") <= 50 && dometurned < 180 && safedistance == False):
				motors.turndome(1)
				dometurned = dometurned + 1
				if(sensors.distance("dome") > 50):
					safedistance == True
			if(safedistance == False)
				motors.resetdome()
				dometurned = 0
				while(sensors.distance("dome") <= 50 && dometurned > -180 && safedistance == False):
					motors.turndome(-1)
					dometurned = dometurned - 1
					if(sensors.distance("dome") > 50):
						safedistance = True
			if(safedistance == False):
				return -1

			# Take the calculate action
			motors.resetdome()
			motors.turnbody(dometurned)

			# Proceed
			motors.drive("forward")

		# Check if the room is light or dark, and enable the bright LED's in the holoprojectors accordingly
		if(sensors.light() == "dark"):
			lights.turnon("all")
			sound.playrandom()
			camera.takepicture()
		if(sensors.light() == "light"):
			lights.turnoff("all")
			sound.playrandom()

		# Check if anyone is talking or if there are any noises
		if(sensors.microphone("overall") == 1):

			# If anyone says anything, we want to calculate where he/she is
			# To do this, we need the timing of all (two or three) microphones,
			# So we can calculate the distance relatively to the object and the distance difference
			# Then, using Pythagoras, we can calculate where the person is, and turn the droid towards him/her

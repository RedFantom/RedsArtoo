# Necessary imports for the program. This version is made on the RPi
import time
import random
import system from os
import sys
import RPi.GPIO as GPIO

# Class for the sensors
class sensors:
    def light(position):
        if(position == 1):
                return GPIO.input(16)
        if(position == 2):
                return GPIO.input(17)
        if(position == 3):
                return GPIO.input(18)

    def distance(position):
        if(position == 'b'):

'''
Important!
'''

class functions:
    def setup():
        # Setup the pins according to the function
        TRIGB = 1
        ECHOB = 2
        TRIGD = 3
        ECHOB = 4

        MOTORL+ = 5
        MOTORL- = 6
        MOTORR+ = 7
        MOTORR- = 8
        MOTORD+ = 9
        MOTORD- = 10

        LIGHT1 = 11
        LIGHT2 = 12
        LIGHT3 = 13

        RGB1R = 14
        RGB1G = 15
        RGB1B = 16

        RGB2R = 17
        RGB2G = 18
        RGB2B = 19

        SPOT1 = 20
        SPOT2 = 21
        SPOT3 = 22

        PWM = 23

        GPIO.setup(TRIGB, GPIO.OUT)
        GPIO.setup(TRIGD, GPIO.OUT)
        GPIO.setup(MOTORL+, GPIO.OUT)
        GPIO.setup(MOTORL-, GPIO.OUT)
        GPIO.setup(MOTORR+, GPIO.OUT)
        GPIO.setup(MOTORR-, GPIO.OUT)
        GPIO.setup(MOTORD+, GPIO.OUT)
        GPIO.setup(MOTORD-, GPIO.OUT)
        GPIO.setup(RGB1R, GPIO.OUT)
        GPIO.setup(RGB1G, GPIO.OUT)
        GPIO.setup(RGB1B, GPIO.OUT)
        GPIO.setup(RGB2R, GPIO.OUT)
        GPIO.setup(RGB2G, GPIO.OUT)
        GPIO.setup(RGB2B, GPIO.OUT)
        GPIO.setup(SPOT1, GPIO.OUT)
        GPIO.setup(SPOT2, GPIO.OUT)
        GPIO.setup(SPOT3, GPIO.OUT)
        GPIO.setup(PWM, GPIO.OUT)

        GPIO.setup(ECHOB, GPIO.IN)
        GPIO.setup(ECHOD, GPIO.IN)
        GPIO.setup(LIGHT1, GPIO.IN)
        GPIO.setup(LIGHT2, GPIO.IN)
        GPIO.setup(LIGHT3, GPIO.IN)

        GPIO.output(TRIGB, False)
        GPIO.output(TRIGD, False)
        GPIO.output(MOTORL+, False)
        GPIO.output(MOTORL-, False)
        GPIO.output(MOTORR+, False)
        GPIO.output(MOTORR-, False)
        GPIO.output(MOTORD+, False)
        GPIO.output(MOTORD-, False)
        GPIO.output(RGB1R, False)
        GPIO.output(RGB1G, False)
        GPIO.output(RGB1B, False)
        GPIO.output(RGB2R, False)
        GPIO.output(RGB2G, False)
        GPIO.output(RGB2B, False)
        GPIO.output(SPOT1, False)
        GPIO.output(SPOT2, False)
        GPIO.output(SPOT3, False)
        GPIO.output(PWM, False)

        os.system("sudo xboxdrv --silent")

    def cleanup():
        GPIO.cleanup()
        sys.exit()
        
    def remotecontrolcheck():

class remotecontrol:


class lights:


class motors:


class autonomous:

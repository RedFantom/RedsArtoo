import time
import RPi.GPIO as GPIO


class motors:  # pinpos and pinneg are pins on which the terminals from the motor driver are connected on the Raspberry Pi

    # Shared Values
    pinpos = 0
    pinneg = 0

    # Constructor to set up the motor
    def __init__(self, pinpos, pinneg):
        GPIO.setup(pinpos, GPIO.OUT)
        GPIO.setup(pinneg, GPIO.OUT)
        self.pinpos = pinpos
        self.pinneg = pinneg

    def pwm(self, speed, state):
        starttime = time.time()
        self.setstate(state)
        time.sleep(0.02 * speed)
        self.setstate(0)
        time.sleep(0.02 * (1.0 - speed))

    # The function that starts and stops the motor
    def setstate(self, direction):
        if direction == 1:
            GPIO.output(self.pinpos, True)
            GPIO.output(self.pinneg, False)
        elif direction == -1:
            GPIO.output(self.pinneg, True)
            GPIO.output(self.pinpos, False)
        elif direction == 0:
            GPIO.output(self.pinpos, False)
            GPIO.output(self.pinneg, False)
        else:
            return -1

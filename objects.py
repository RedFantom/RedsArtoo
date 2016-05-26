import motors
import sensors
import lights
import RPi.GPIO as GPIO
import smbus
import neopixel

# Pins on the Raspberry Pi B+, GPIO.BCM
DistanceSensorOneTrig   =  4
DistanceSensorOneEcho   = 17
DistanceSensorTwoTrig   = 18
DistanceSensorTwoEcho   = 23

SensorOnePWMpin         = 0
SensorTwoPWMpin         = 0
SensorAmountOfLeds      = 4
SpotLightOnePin         = 0
SpotLightTwoPin         = 0

OnOffSwitch             = 25

MotorDomeOne            = 5
MotorDomeTwo            = 6
MotorLeftOne            = 12
MotorLeftTwo            = 13
MotorRightOne           = 19
MotorRightTwo           = 26

ShutdownSwitch          = 0
BatterySensor           = 0

# The UART pins are GPIO 14 and 15
# The SPI pins are GPIO 10 (MOSI), 9 (MISO), 11 (CLOCK), 8 (CE0_N) and 7 (CE1_N)
# The I2C pins are GPIO 2 (SDA) and 3 (SCL)

SoundSensorOnePin = 0
SoundSensorTwoPin = 0
SoundSensorThreePin = 0

# I2C addresses, not checked yet, just examples, you can read them using I2C detect
bus = smbus.SMBus(1)
AcceleroMeterAddress = 0x68

# The motors run at a certain speeds, this value is in degrees per second when one motor is running at full speed
TurningRate = 1
# The speed the droid travels at when at full speed in forward direction in cm/sec
TravelSpeed = 1
# Since I've decided to use a Raspberry Pi Zero instead of an MCP20317 chip, the pinout has changed
# I'll decide what pins to use as soon as I get the chance
# Because the Pi Zero has more GPIO pins than an MCP20317, I might give the motors two speeds
# Using PWM would be a possibility too, but the motor controller themselves already use PWM, so it would be using PWM to control a PWM controller

GPIO.setmode(GPIO.BCM)

DistanceSensorOne = sensors.distancesensor(DistanceSensorOneTrig, DistanceSensorOneEcho)
DistanceSensorTwo = sensors.distancesensor(DistanceSensorTwoTrig, DistanceSensorTwoEcho)

SensorOne = neopixel.Adafruit_NeoPixel(SensorAmountOfLeds, SensorOnePWMpin, 800000, 5, False)
SensorTwo = neopixel.Adafruit_NeoPixel(SensorAmountOfLeds, SensorTwoPWMpin, 800000, 5, False)

SpotLightOne = lights.spotlight(SpotLightOnePin)
SpotLightTwo = lights.spotlight(SpotLightTwoPin)

MotorDome = motors.motors(MotorDomeOne, MotorDomeTwo)
MotorLeft = motors.motors(MotorLeftOne, MotorLeftTwo)
MotorRight = motors.motors(MotorRightOne, MotorRightTwo)

SoundSensorOne = sensors.soundsensor(SoundSensorOnePin)
SoundSensorTwo = sensors.soundsensor(SoundSensorTwoPin)
SoundSensorThree = sensors.soundsensor(SoundSensorThreePin)

DistanceProcess = multiprocessing.Process(target = distance)
ShutdownRequesterProcess = multiprocessing.Process(target = ShutdownRequester)
CompassProcess = multiprocessing.Process(target = compass)
AccelerometerProcess = multiprocessing.Process(target = Accelerometer)

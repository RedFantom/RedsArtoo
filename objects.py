# Pins on the Raspberry Pi B+, GPIO.BCM
DistanceSensorOneTrig   =  4
DistanceSensorOneEcho   = 17
DistanceSensorTwoTrig   = 18
DistanceSensorTwoEcho   = 23

SensorOneRed            = 27
SensorOneGreen          = 22
SensorOneBlue           = 24
SensorTwoRed            = 16
SensorTwoGreen          = 20
SensorTwoBlue           = 21

MotorDomePos            = 5
MotorDomeNeg            = 6
MotorLeftPos            = 12
MotorLeftNeg            = 13
MotorRightPos           = 19
MotorRightNeg           = 26

OnOffSwitch             = 25

# The UART pins are GPIO 14 and 15
# The SPI pins are GPIO 10 (MOSI), 9 (MISO), 11 (CLOCK), 8 (CE0_N) and 7 (CE1_N)
# The I2C pins are GPIO 2 (SDA) and 3 (SCL)

# Since I've decided to use a Raspberry Pi Zero instead of an MCP20317 chip, the pinout has changed
# I'll decide what pins to use as soon as I get the chance
# Because the Pi Zero has more GPIO pins than an MCP20317, I might give the motors two speeds
# Using PWM would be a possibility too, but the motor controller themselves already use PWM, so it would be using PWM to control a PWM controller

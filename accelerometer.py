import smbus
import math
import objects

# Registers for power management
PowerManagementOne = 0x06b
PowermanagementTwo = 0x06c

# The following functions I got from the Bitify blog. I have rewritten them to suit my style
def ReadByte(adr):
    return objects.bus.read_byte_data(objects.address, adr)

def ReadWord(adr):
    high = objects.bus.read_byte_data(address, adr)
    low  = objects.bus.read_byte_data(address, adr + 1)
    value = (high << 8) + low
    return value

def ReadWord2C(adr):
    value = ReadWord(adr)
    if(value >= 0x8000):
        return -((65535 - value) + 1)
    else:
        return value

def pythagoras(a, b):
    return math.sqrt((a * a) + (b * b))

def yRotation(x, y, z):
    radians = math.atan2(x, pythagoras(y, z))
    return -math.degrees(radians)

def xRotation(x, y, z):
    radians = math.atan2(y, pythagoras(x, z))
    return math.degrees(radians)

def wake():
    objects.bus.write_byte_data(objects.address, PowerManagementOne, 0)

GyroX = ReadWord2C(0x43) / 131
GyroY = ReadWord2C(0x45) / 131
GyroZ = ReadWord2C(0x47) / 131

AccelX = ReadWord2C(0x3b) / 16384.0
AccelY = ReadWord2C(0x3d) / 16384.0
AccelZ = ReadWord2C(0x3f) / 16384.0

xRotationValue = xRotation(AccelX, AccelY, AccelZ)
yRotationVAlue = yRotation(AccelX, AccelY, AccelZ)

def update():
    wake()
    GyroX = ReadWord2C(0x43) / 131
    GyroY = ReadWord2C(0x45) / 131
    GyroZ = ReadWord2C(0x47) / 131

    AccelX = ReadWord2C(0x3b) / 16384.0
    AccelY = ReadWord2C(0x3d) / 16384.0
    AccelZ = ReadWord2C(0x3f) / 16384.0

    xRotationValue = xRotation(AccelX, AccelY, AccelZ)
    yRotationVAlue = yRotation(AccelX, AccelY, AccelZ)

import random

def setup(pin, function, type):
    print pin, "has now been setup with", function, "and", type

def cleanup():
    print "All pins have now been cleared"

def output(pin, out):
    print pin, "has now been turned", out

def input(pin):
    randomint = randint(0, 1)
    if(randomint == 0):
        randombool = False
    else:
        randombool = True
    print pin, "has now gotten", randombool
    return randombool

def setmode(mode):
    print "The board has now gotten mode ", mode

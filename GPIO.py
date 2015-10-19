import random

OUT = "output"
IN = "INPUT"
BCM = "BCM"


def setup(pin, function, type):
    print pin, "now has function", function, "with", type

def cleanup():
    print "All pins have now been cleaned"

def output(pin, status):
    print pin, "has now been turned", status

def input(pin):
    return random.choice([True, False])

def setmode(mode):
    print "Now been set to", mode

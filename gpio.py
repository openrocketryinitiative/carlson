# Carlson GPIO control
#
# Benjamin Shanahan

import RPi.GPIO as GPIO

OUTPUT = GPIO.OUT
INPUT  = GPIO.IN
HIGH   = GPIO.HIGH
LOW    = GPIO.LOW

class Pin:

    def __init__(self, pin, direction=OUTPUT, state=LOW):
        self.pin = pin
        self.direction = direction
        self.state = state
        self._init_pin()

    def toggle(self):
        GPIO.output(self.pin, 1-self.state)

    def set_high(self):
        GPIO.output(self.pin, HIGH)

    def set_low(self):
        GPIO.output(self.pin, LOW)

    def _init_pin(self):
        GPIO.setwarnings(False)  # Turn off GPIO library warnings
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(self.pin, self.direction)
        GPIO.output(self.pin, self.state)
        print "Initialized GPIO pin %d." % self.pin

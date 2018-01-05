# State class
#
# Benjamin Shanahan

class State:

    def __init__(self):

        # Define states and their bit positions
        self.IDLE          = 0    # default state on rocket boot

        self.ARM           = 1    # arm / disarm rocket and allow other functionality
        self.ARM_BIT       = 0    # bit position

        self.LOGGING       = 2    # start / stop logging sensor and camera data
        self.LOGGING_BIT   = 1 

        self.CHUTE         = 4    # toggle parachute GPIO pin
        self.CHUTE_BIT     = 2

        self.POWER_OFF     = 8    # shut down Carlson computer
        self.POWER_OFF_BIT = 3

        self.FREEFALL      = 16   # accelerometers detected freefall condition
        self.FREEFALL_BIT  = 4

        self.APOGEE        = 32   # rotation greater than 90 deg from vertical, deploy chute
        self.APOGEE_BIT    = 5

        # Define state value holder
        self.state = self.IDLE

    # Set state
    def set(self, new_state):
        self.state = new_state

    # Add state (input each state as separate parameter)
    def add(self, *new_states):
        for new_state in new_states:
            self.state += new_state

    # Remove state
    def remove(self, *new_states):
        for new_state in new_states:
            self.state -= new_state

    # Retrieve value of bit at index in state. Return True if bit is 1. If a
    # value for byte is specified, the bit is checked in that, not in state.
    def get_bit(self, idx, byte=None):
        if byte is None:
            return ((self.state & (1 << idx)) != 0);
        else:
            return ((byte & (1 << idx)) != 0);

    # Return state as string
    def __str__(self):
        # If we are idle, return
        if self.state == self.IDLE:
            return "Idle"
        # Otherwise, parse out the flags
        ret = ""
        if self.get_bit(self.ARM_BIT):       ret += "Armed + "
        if self.get_bit(self.LOGGING_BIT):   ret += "Logging + "
        if self.get_bit(self.FREEFALL_BIT):  ret += "Freefall + "
        if self.get_bit(self.APOGEE_BIT):    ret += "Apogee + "
        if self.get_bit(self.CHUTE_BIT):     ret += "Deployed Chute + "
        if self.get_bit(self.POWER_OFF_BIT): ret += "Powering Off + "
        return ret[:-3]

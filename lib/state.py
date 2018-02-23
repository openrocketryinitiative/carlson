# State class
#
# Benjamin Shanahan

class State:
    """Define different rocket states and provide a convenient interface.

    The defined states each have an assigned bit. This bit corresponds a bit in
    the command byte. When sending commands between GROUND and AIR, we want to
    minimize the amount of data transmitted across the radios. To do this, we 
    only send a single byte, where each of the 8 bits encodes a different 
    active state. For example, if we send a `7`, this is `0000 0111` in binary,
    and this means that bits 0, 1, and 2 are high (right to left): i.e. ARM + 
    LOGGER + CHUTE.
    """

    def __init__(self):

        # Define states and their bit positions in a byte
        self.IDLE          = 0  # default, no bits high

        # arm / disarm rocket and allow other functionality
        self.ARM           = 1
        self.ARM_BIT       = 0

        # start / stop logging sensor and camera data
        self.LOGGING       = 2
        self.LOGGING_BIT   = 1 

        # toggle parachute GPIO pin
        self.CHUTE         = 4
        self.CHUTE_BIT     = 2

        # shut down Carlson computer
        self.POWER_OFF     = 8
        self.POWER_OFF_BIT = 3

        # accelerometers detected freefall condition
        self.FREEFALL      = 16
        self.FREEFALL_BIT  = 4

        # rotation greater than 90 deg from vertical, deploy chute
        self.APOGEE        = 32
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
        return ret[:-3]  # remove trailing ' + '
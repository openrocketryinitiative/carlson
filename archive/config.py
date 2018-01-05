###############################################################################
## Rocket States
###############################################################################

class State:

    def __init__(self):

        # Define states and their bit positions
        self.IDLE          = 0    # default state on rocket boot

        self.ARM           = 1    # arm / disarm rocket and allow other functionality
        self.ARM_BIT       = 0    # bit position

        self.DATA          = 2    # start / stop recording sensor data to disk
        self.DATA_BIT      = 1 

        self.VIDEO         = 4    # start / stop camera capture
        self.VIDEO_BIT     = 2

        self.CHUTE         = 8    # toggle parachute GPIO pin
        self.CHUTE_BIT     = 3

        self.POWER_OFF     = 16   # shut down computer (last possible state)
        self.POWER_OFF_BIT = 4 

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
        if self.get_bit(self.DATA_BIT):      ret += "Recording Data + "
        if self.get_bit(self.VIDEO_BIT):     ret += "Recording Video + "
        if self.get_bit(self.CHUTE_BIT):     ret += "Deployed Chute + "
        if self.get_bit(self.POWER_OFF_BIT): ret += "Powering Off + "
        return ret[:-3]

###############################################################################
## Sensors and IO
###############################################################################

class Sensor:

    RTIMU_INI_FILE      = "RTIMULib"
    CHUTE_PIN           = 4
    BLAST_CAP_BURN_TIME = 5  # seconds

###############################################################################
## Telemetry
###############################################################################

class Telemetry:

    PORT                = "/dev/ttyUSB0"
    BAUD                = 57600
    SERIAL_TIMEOUT      = 0
    TIME_BEFORE_RESEND  = 0.5  # (s) how long to wait before panicking (send again)
    HEARTBEAT_DELAY     = 1    # (s) delay between heartbeats
    HEARTBEAT_MAX_DELAY = 3    # (s) max delay between heartbeats before panic

    # Telemetry commands
    HEARTBEAT = "H"
    ARM       = "a"
    DEPLOY    = "d"
    STOP      = "x"
    HELP      = "h"
    QUIT      = "q"
    NOPE      = "0"  # I got your command, but I'm not executing it
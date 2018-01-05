# Telemetry radio stuff
#
# Benjamin Shanahan

import serial
import time

PORT               = "/dev/ttyS0"
BAUD               = 57600
SERIAL_TIMEOUT     = 0
TIME_BEFORE_RESEND = 0.5  # (s) how long to wait before panicking (send again)

class Telemetry:

    def __init__(self, port=PORT, baud=BAUD, timeout=SERIAL_TIMEOUT):
        self.radio = None
        self._initialize_telemetry(port, baud, timeout)

    def write(self, data):
        self.radio.write(data)

    def read(self, n_bytes=1):
        return self.radio.read(n_bytes)

    # Try to connect to radio at given port
    def _initialize_telemetry(self, port=PORT, baud=BAUD, timeout=SERIAL_TIMEOUT):
        while True:
            try:
                self.radio = serial.Serial(port=port, baudrate=baud, timeout=timeout)
                print "Initialized telemetry radio."
                return True
            except serial.serialutil.SerialException:
                print "Radio not found, trying again. Did you run as `sudo`?"
                time.sleep(1)

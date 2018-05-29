"""Carlson AIR / GROUND station parameters.
"""

HEARTBEAT_DELAY          = 1     # s, how often do we send state to ground station

BLAST_CAP_BURN_TIME      = 5     # s, how long to keep relay shorted for

FREEFALL_ACCEL_THRESH    = 0.3   # G, maximum absolute acceleration allowed on all axes for freefall detection
FREEFALL_COUNTER_THRESH  = 20    # number of consecutive freefall detections before flag is set True

AUTO_APOGEE_DETECT       = True  # should we use our auto-apogee detection algorithm to control the chute?
APOGEE_ANGLE_THRESH      = 5     # deg, angle in degrees combined rocket roll pitch at which we deploy chute
APOGEE_COUNTER_THRESH    = 20    # number of consecutive apogee detections before we deploy the chute

# Should we debug?
LOG_DEBUG   = True    # Save debug info to a local text file
LOCAL_DEBUG = False   # Print IMU data to terminal directly. Only use if ssh'd into Carlson directly.

# Stabilization
# PID parameters
YAW_PID = (0.03, 0.0, 0.0)
RP_PID  = (0.05, 0.0, 0.0)

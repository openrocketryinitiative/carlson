#!/usr/bin/python

# Carlson AIR station v0.3
#
# 5 October 2017, Benjamin Shanahan.

import time
import serial
import os

import logger as lgr
import wirelesscommunicator as wc
import numpy as np
from math import sqrt
from state import State
from telemetry import Telemetry
from sensor import Sensor
from gpio import Pin

HEARTBEAT_DELAY          = 1     # s, how often do we send state to ground station

BLAST_CAP_BURN_TIME      = 5     # s, how long to keep relay shorted for

FREEFALL_ACCEL_THRESH    = 0.3   # G, maximum absolute acceleration allowed on all axes for freefall detection
FREEFALL_COUNTER_THRESH  = 20    # number of consecutive freefall detections before flag is set True

AUTO_APOGEE_DETECT       = True  # should we use our auto-apogee detection algorithm to control the chute?
APOGEE_ANGLE_THRESH      = 5     # deg, angle in degrees combined rocket roll pitch at which we deploy chute
APOGEE_COUNTER_THRESH    = 20    # number of consecutive apogee detections before we deploy the chute

# Should we debug?
LOG_DEBUG   = True   # Save debug info to a local text file
# TODO: **important** THIS OPTION (UDP_DEBUG) SHOULD BE FALSE UNLESS MANUALLY SPECIFIED BY A FLAG (ARGPARSER)
UDP_DEBUG   = True   # Send info across network to another machine on the network
LOCAL_DEBUG = True   # Print IMU data to terminal directly. Only use if ssh'd into Carlson directly.

def rad2deg(rad):
    return rad * 57.2958

if __name__ == "__main__":

    # Bit latches
    arm                 = False
    logging             = False
    deploy_chute        = False
    power_off           = False

    # Current state latches
    _armed              = False  # Rocket is armed.
    _logging_on         = False  # Data logging from IMU is on.
    _freefall_detected  = False  # Rocket motor is not thrusting (rocket is in freefall).
    _chute_deployed     = False  # Parachute is deployed.
    _nicrome_on         = False  # Nicrome wire is heating.
    _apogee_detected    = False  # Algorithm detects that apogee is reached.

    # Set current state of air controller and declare the time we last sent a 
    # state update to the ground station
    state               = State()
    state_last_sent     = 0

    # Timing / counting variables
    time_chute_deployed = 0
    freefall_counter    = 0
    apogee_counter      = 0

    ###########################################################################
    ## Initialize Wireless Communication
    ###########################################################################

    # TODO: allow IPs and ports to be specified via argparser
    if UDP_DEBUG:
        host_port   = 5000             # Carlson's port (local)
        target_ip   = "192.168.1.228"  # IP of laptop running WIFIDEBUGGER
        target_port = 5001             # Port on laptop running WIFIDEBUGGER
        try:
            wifidebugger = wc.WirelessCommunicator(
                host_port=host_port, target_ip=target_ip, target_port=target_port)
            UDP_DEBUG_SOCKET_INIT_OK = True
        except:
            print "Failed to bind port for WiFi debugging, skipping."
            UDP_DEBUG_SOCKET_INIT_OK = False

    ###########################################################################
    ## Initialize our external devices
    ###########################################################################

    # Define logger but don't initialize a new log file here
    logger = lgr.Logger(init_log=False, init_camera=False, init_debug=True)

    # Define debug function
    def debug(text):
        if LOG_DEBUG: logger.write(text, lgr.DEBUG)

    # TODO: reorganize this; add UDP WiFi debugger status to debug file
    if UDP_DEBUG and UDP_DEBUG_SOCKET_INIT_OK: 
        debug("UDP debugger initialized OK")
    else:
        debug("UDP debugger failed to initialize")

    # Initialize telemetry radio for communication with ground station
    radio = Telemetry()
    debug("Initialized telemetry.")

    # Initialize the IMU and barometer sensors so that we can read from them
    sensor = Sensor()
    debug("Initialized sensor.")

    # Initialize the GPIO pins so that we can write them high or low
    chute_pin = Pin(4)
    debug("Initialized chute pin.")

    # Inline function definitions to control chute pin behavior. Note the 
    # unfortunate global scoping: apparently Python won't allow inline
    # functions to modify (only read) variables from outer scopes. In order
    # to modify the variables, we need to force a global scope.
    def trigger_chute_pin():
        global chute_pin, _nicrome_on, _chute_deployed, time_chute_deployed
        chute_pin.set_high()
        _nicrome_on = True
        _chute_deployed = True
        time_chute_deployed = time.time()
        debug("Chute pin HIGH")
        print "Set chute pin to HIGH"
    def untrigger_chute_pin():
        global chute_pin, _nicrome_on
        chute_pin.set_low()
        _nicrome_on = False
        debug("Chute pin LOW")
        print "Set chute pin to LOW"

    # Main loop
    t0 = 0
    debug("Entering program loop.")
    while (True):

        #######################################################################
        ## Interpret state information from GROUND station
        #######################################################################

        new_state = radio.read();
        
        # If we got a state command via telemetry, parse it and set latches
        if new_state != "":
            new_state = ord(new_state)  # convert from char to int
            debug("New state read (%d)." % new_state)

            # Get bit flags from new state
            arm       = state.get_bit(state.ARM_BIT, byte=new_state)
            logging   = state.get_bit(state.LOGGING_BIT, byte=new_state)
            chute     = state.get_bit(state.CHUTE_BIT, byte=new_state)
            power_off = state.get_bit(state.POWER_OFF_BIT, byte=new_state)

            ### Arm rocket ###
            if arm:
                if not _armed:
                    _armed = True
                    debug("Armed")
                    print "Armed"
            else:
                if _armed:
                    _armed = False
                    _chute_deployed = False
                    _freefall_detected = False
                    _apogee_detected = False
                    freefall_counter = 0
                    apogee_counter = 0
                    debug("Disarmed")
                    print "Disarmed"

            ### Data logging (sensor data and video) ###
            if logging:
                if not _logging_on:
                    # Initialize logger, which will create a new log file and
                    # set up the camera so we're ready to record. Start the
                    # camera too.
                    logger._init_new_log()
                    logger.start_video()  # will only do something if camera's enabled
                    t0 = time.time()  # reset reference time
                    _logging_on = True
                    debug("Started logging")
                    print "Started logging"
            else:
                if _logging_on:
                    # Stop data and camera and safely close file on disk.
                    logger.stop()  # stop only LOG, not DEBUG
                    _logging_on = False
                    debug("Stopped logging")
                    print "Stopped logging"

            ### Deploy chute ###
            if chute:
                if not _chute_deployed and _armed:
                    trigger_chute_pin()

            ### Power off ###
            if power_off:
                if not _armed and not _logging_on:
                    print "Powering off"
                    debug("Power off")
                    logger.stop(target=DEBUG)  # flush and close debug file
                    os.system("sudo poweroff")

        #######################################################################
        ## Do repeated actions (i.e. read from sensors) depending on latches
        #######################################################################
        
        # If logging is on, write IMU data to logfile! We have yet to implement
        # sensor logging from the BMP280 because its read speed is slower than
        # from the IMU.
        #
        # We are currently logging 14 data points, which will be transmitted as
        # 4-byte floats across the wireless network during UDP debugging. This
        # is 4*14 = 56 bytes (plus header) per UDP packet.
        if _logging_on:
            # Read from IMU
            data = sensor.read_imu()
            if data is not None:
                t = time.time() - t0
                debug("[%s] Data read" % t)
                data_vector = [t, state.state,
                    data["fusionPose"][0], data["fusionPose"][1], data["fusionPose"][2],
                    data["compass"][0],    data["compass"][1],    data["compass"][2],
                    data["accel"][0],      data["accel"][1],      data["accel"][2],
                    data["gyro"][0],       data["gyro"][1],       data["gyro"][2]]
                logger.write(data_vector)

                # Freefall detection algorithm. During freefall the 
                # accelerometer will read zero acceleration on all axes -- this
                # is because although the force of gravity is acting on the 
                # rocket making it fall, the accelerometer itself is 
                # accelerating towards the center of the Earth, so the 
                # acceleration of the internal components is equal to that of 
                # the external ones, measuring zero acceleration. To detect 
                # this freefall condition, we calculate the norm of the rocket
                # acceleration vector and when it goes below a threshold of
                # FREEFALL_ACCEL_THRESH for FREEFALL_COUNTER_THRESH samples, we
                # consider the rocket to be in freefall.
                accel_norm = sqrt( \
                    data["accel"][0]**2 + data["accel"][1]**2 + data["accel"][2]**2)
                if accel_norm < FREEFALL_ACCEL_THRESH:
                    freefall_counter += 1
                    if freefall_counter > FREEFALL_COUNTER_THRESH:
                        _freefall_detected = True
                else:
                    freefall_counter = 0

                # Apogee detection algorithm. Theta is the angle of deviation 
                # from the rocket's initial vertical position. When theta goes 
                # below APOGEE_ANGLE_THRESH for more than APOGEE_COUNTER_THRESH
                # samples, the _apogee_detected flag is set high and the chute
                # pin is triggered to light the blast cap nicrome.
                theta = np.degrees(np.arcsin(
                    np.cos(data["fusionPose"][0]) * np.cos(data["fusionPose"][1])))
                if _freefall_detected:
                    if theta < APOGEE_ANGLE_THRESH:
                        apogee_counter += 1
                        if apogee_counter > APOGEE_COUNTER_THRESH:
                            _apogee_detected = True
                    else:
                        apogee_counter = 0
                
                # If wifi debugging is enabled, send the data over UDP.
                if UDP_DEBUG and UDP_DEBUG_SOCKET_INIT_OK:
                    # Try to send data over UDP, if it fails, just skip, we don't want
                    # any other part of the code to stop.
                    try:
                        wifidebugger.send(data_vector)
                    except:
                        pass

                # If local debugging is enabled, print to terminal directly.
                if LOCAL_DEBUG:
                    #print "accel: %.2f %.2f %.2f" % (data["accel"])

                    #print "_freefall_detected:", _freefall_detected, \
                    #        "_apogee_detected:", _apogee_detected

                    print "R: %.2f  P: %.2f  Y: %.2f  ACC_NORM: %.2f  ANGLE: %.2f  FREEFALL: %s  APOGEE: %s" % \
                           (rad2deg(data["fusionPose"][0]),
                           rad2deg(data["fusionPose"][1]),
                           rad2deg(data["fusionPose"][2]),
                           accel_norm, theta, _freefall_detected, _apogee_detected)

        # Set chute pin high if we are using automatic apogee detection algorithm.
        if AUTO_APOGEE_DETECT and _freefall_detected and _armed:
            if _apogee_detected and not _chute_deployed:
                trigger_chute_pin()

        # Set chute pin back to LOW if blast cap burn time is reached
        if _nicrome_on and (time.time() - time_chute_deployed > BLAST_CAP_BURN_TIME):
            untrigger_chute_pin()

        #######################################################################
        ## Update GROUND station
        #######################################################################

        # Update ground station once per HEARTBEAT_DELAY
        if time.time() - state_last_sent > HEARTBEAT_DELAY:
            state.set(state.IDLE)  # clear state and rebuild
            if _armed:             state.add(state.ARM)
            if _logging_on:        state.add(state.LOGGING)
            if _chute_deployed:    state.add(state.CHUTE)
            if _freefall_detected: state.add(state.FREEFALL)
            if _apogee_detected:   state.add(state.APOGEE)
            radio.write(chr(state.state))
            state_last_sent = time.time()
            debug("Sent heartbeat (%d)" % state.state)

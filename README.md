# Carlson v0.3

Carlson is a Raspberry Pi Zero based rocket flight computer with an MPU9255 IMU, BMP280 barometer, 1080p video camera, WiFi chip, and 915 MHz telemetry radio. It runs on a two-cell lithium polymer battery. Carlson will eventually control automatic apogee detection in flight and parachute deployment.

## Installation 

**GROUND**

    $ pip install -r requirements/ground.txt

**AIR**

Follow directions under *Additional Repositories* below to compile and install sensor libraries. Then,

    $ pip install -r requirements/air.txt

***IMPORTANT***: If you are using a Raspberry Pi to host AIR.py, please make sure that I2C and Serial hardware are enabled and 'login shell over serial' is disabled. These options can be configured in *Interfacing Options* in `sudo raspi-config`.

## AIR station 

Python state machine running on the Raspberry Pi in the rocket that starts and stops data / video logging and can detonate the parachute ejection blast cap in flight. This script sends periodic updates to the GROUND station via telemetry at 1 Hz and listens for incoming state transition commands from GROUND. 

## GROUND station 

Python ground server script. This is a lite version of what will eventually run on the base station, controlled by the web server (a user will interact with the system through a front-end web-page server by the web server, allowing increased distance from the launch site for increased safety). The ground script serves up an input terminal where user can manually input commands. Data received from the AIR station is printed in the terminal as soon as it arrives.

#### Available Commands

Coming soon. For now, just check out the GROUND.py source code.

## Additional Repositories 

These repositories have been forked so that we can modify them as required. They both require compilation and installation before they can be used.

### Accel/Gyro/Magnet 

https://github.com/benshanahan1/RTIMULib2

For compilation on Linux systems, see https://github.com/benshanahan1/RTIMULib2/tree/master/Linux.

### Barometer 

https://github.com/benshanahan1/BMP280

This is just a C++ python library that needs to be compiled. Run:

	$ sudo python setup.py build
	$ sudo python setup.py install

## Telemetry Link 

We are using a pair of 915 MHz 3DR telemetry radios to communicate between AIR and GROUND. This radio link enables two-way communication between the AIR and GROUND stations.

## Carlson Launch Checklists 

#### @ Home Base 

- Charge batteries (2-cell LiPo's are full at 4.2 V*2 cells = 8.4 V)
- Power flight computer on, run full test of GROUND and AIR station code (verify state changes, camera, logging, etc.); check connection wires are intact
- Install flight computer in rocket body
- Set IMU orientation in RTIMULib.ini file (see AxisRotation flag in file)
- Recalibrate IMU (if needed) (run `cd carlson` and then `RTIMULibCal` and follow the instructions) (if recalibration is needed, it's not a bad idea to back up the calibration file: `cp RTIMULib.ini reference/calibration/RTIMULib.ini.bak`)
- SSH in (`ssh pi@carlson.local`) and test logging / parachute (check that log file and video have data in them, run `python ~/RTIMULib2/Linux/python/tests/Fusion.py` to see that IMU is working -- it should spit out non-zeros values at 80 Hz that change when you move the IMU)
- In video footage, verify that in video the camera is not obstructed by rocket body
- Check parachute string for breakage; replace / repair if needed
- Set up helper Pi as wireless access point and configure Carlson to connect to this network as a client automatically
- Pack the nichrome wire, Pi configured as access point, USB micro cable, blast cap, wadding, parachute, string, and ejection fuel!

#### @ Launch Site 

- Power on helper Pi hosting wireless access point
- Connect to helper Pi's access point with laptop
- Power on Carlson, SSH in over access point, run GROUND and AIR stations, switch through different states to test logging and chute deployment logic; verify that relay clicks when chute is deployed from GROUND station
- Run `bash carlson/resource/scp_log_video` to scp all Carlson log and video data to desktop, verify that data is all there and working properly
- Restart AIR python script on Carlson and start logger (IMU data and video capture)
- Blast off

## To Do 

1. Calibrate IMU before next flight (check orientation flags for mounting in rocket)
2. Update requirements/air.txt
3. Incorporate barometer data

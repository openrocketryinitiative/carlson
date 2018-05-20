# Carlson sensor class to manage sensor initialization and logging
#
# Benjamin Shanahan & Elias Berkowitz

import time

import RTIMU
from threading import Thread, Lock
from BMP280 import BMP280

RTIMU_INI_FILE = "config/RTIMULib"

class Sensor:
    """Interface with WaveShare MPU-9255 IMU using RTIMU and BMP280 libraries.
    """

    def __init__(self, configFile=RTIMU_INI_FILE):
        # Make sure config file path is OK
        if configFile[-4:] == ".ini":
            raise Exception("Please do not include the '.ini' in the config filename.")
        self._init_imu(configFile)
        # self._init_barometer()
        self.thread         = Thread(target=self.spin)
        self.thread.daemon  = True
        self.thread_running = True
        self.thread_lock    = Lock()
        self._imu_data      = None

    def start(self):
        """Start thread to pull data from the IMU.
        """
        self.thread.start()
        print("Started sensor reading thread.")

    def stop(self):
        """Stop thread IMU data pulling thread.
        """
        self.thread_running = False
        print("Stopped sensor reading thread.")

    @property
    def imu_data(self):
        """Acquire thread lock and grab latest IMU Data.
        """
        return_data = None
        self.thread_lock.acquire()
        return_data = self._imu_data
        self.thread_lock.release()
        return return_data

    def spin(self):
        """Threaded function to read from IMU as fast as possible.
        """
        while self.thread_running:
            if self.imu.IMURead():
                data = self.imu.getIMUData()
                self.thread_lock.acquire()
                self._imu_data = data
                self.thread_lock.release()

    # def read_barometer_temperature_pressure(self):
    #     return self.barometer.read_temperature_pressure()

    # def read_barometer_altitude(self):
    #     return self.barometer.read_altitude()

    def _init_imu(self, configFile):
        # Configure IMU and barometer
        self.settings = RTIMU.Settings(configFile)  # calibration file
        self.imu = RTIMU.RTIMU(self.settings)
        if (not self.imu.IMUInit()):
            print "IMU failed to initialize!"
        else:
            print "IMU initialized."

        # Configure some IMU specific settings
        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)

    # def _init_barometer(self):
    #     self.barometer = BMP280.BMP280()
    #     print "Barometer initialized."

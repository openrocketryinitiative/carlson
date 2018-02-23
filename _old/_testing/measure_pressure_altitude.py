#!/usr/bin/python


#SETTINGS FOR I2C_ADRESS
#address=
#BMP280_I2CADDR  = 0x77
#BMP280_I2CADDR2 = 0x76



#SETTINGS FOR TEMPERATURE OVERSAMPLING
#OVER x2 SAMPLE NO USE FOR PRESSURE ACCURANCY
#modet=
#BMP280_T_O1            x1  Sample
#BMP280_T_O2            x2  Sample
#BMP280_T_O4            x4  Sample
#BMP280_T_O8            x8  Sample
#BMP280_T_O16           x16 Sample


#PRESSURE OVERSAMPLING MODES
#modep=
#BMP280_ULTRALOWPOWER   x1  Sample
#BMP280_LOWPOWER        x2  Sample
#BMP280_STANDARD        x4  Sample
#BMP280_HIGHRES         x8  Sample
#BMP280_ULTRAHIGHRES    x16 Sample


#FILTER SETTINGS        >=75% STEP_RESPONCE AFTER SAMPLE
#BMP280_FILTER_OFF      1
#BMP280_FILTER_2        2
#BMP280_FILTER_4        5
#BMP280_FILTER_8        11
#BMP280_FILTER_16       22

#FUNCTIONS:
#_load_calibration(self)
#_set_filter(self)
#_load_datasheet_calibration(self)
#read_raw_temp_pressure(self)
#read_temperature_pressure(self)
#read_altitude(self, sealevel_pa=101325.0)
#read_sealevel_pressure(self, altitude_m=0.0)



import time
import BMP280.BMP280 as BMP280

#setting timeout for 7 hours
#timeout = time.time() + 60*60*7

#Make a file called after the date and time for better order
#file = open(time.strftime("%Y")+time.strftime("%m")+time.strftime("%d")+'-'+time.strftime("%H")+time.strftime("%M")+time.strftime("%S")+'_'+'_measurements.csv','a')
#file.write(time.strftime("%Y")+time.strftime("%m")+time.strftime("%d")+'-'+time.strftime("%H")+time.strftime("%M")+time.strftime("%S")+'\n')

#Initializing the sensor
#sensor = BMP280.BMP280(modep=BMP280.BMP280_ULTRAHIGHRES,modet=BMP280.BMP280_T_O2,filter=BMP280.BMP280_FILTER_OFF,address=BMP280.BMP280_I2CADDR2)
sensor = BMP280.BMP280()

#Setting a start time for better log plots
#st = time.time()
#writing to csv file every 30 seconds
while True:
	#Getting sensor-temp and -pressure
	t1, p1 = sensor.read_temperature_pressure()
        a1     = sensor.read_altitude()
	#Getting corrected pressure for current pressure at sealevel
	#p10 = sensor.read_sealevel_pressure(altitude_m=330.0) 	#Takes new messurement so the sensor_data might have changed
	
        #out=(str(time.time()-st) + ',' + str(t1) + ',' + str(p1) + ',' + str(p10) + '\n')
        #file.write(out)
        #print(out)
        
        #print "temp:", t1, "\tpressure:", p1, "\taltitude:", a1
        print "temp: %.2f, pressure: %.4f, altitude: %0.2f" % (t1, p1, a1)
        time.sleep(.004)
        #if time.time() > timeout:
        #        file.close()
        #        break


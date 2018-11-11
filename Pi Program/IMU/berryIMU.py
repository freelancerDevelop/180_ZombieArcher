#!/usr/bin/python
#
#    This program  reads the angles from the acceleromter and gyroscope
#	 from a BerryIMU connected to a Raspberry Pi.
#
#    This program includes two filters (low pass and median) to improve the 
#    values returned from BerryIMU by reducing noise.
#
#
#    http://ozzmaker.com/
#    Both the BerryIMUv1 and BerryIMUv2 are supported
#
#    BerryIMUv1 uses LSM9DS0 IMU
#    BerryIMUv2 uses LSM9DS1 IMU
#




import sys
import time
import math
import IMU
import datetime
import os
import json

def collect(sensor_socket, ADDRESS, signal):
    # If the IMU is upside down (Skull logo facing up), change this value to 1
    IMU_UPSIDE_DOWN = 0	


    RAD_TO_DEG = 57.29578
    M_PI = 3.14159265358979323846
    G_GAIN = 0.070  	# [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
    AA =  0.40      	# Complementary filter constant
    ACC_LPF_FACTOR = 0.4 	# Low pass filter constant for accelerometer
    ACC_MEDIANTABLESIZE = 9    	# Median filter table size for accelerometer. Higher = smoother but a longer delay



    ################# Calibration values ############
    # Use calibrateBerryIMU.py to get calibration values 


    gyroXangle = 0.0
    gyroYangle = 0.0
    gyroZangle = 0.0
    CFangleX = 0.0
    CFangleY = 0.0
    CFangleXFiltered = 0.0
    CFangleYFiltered = 0.0
    CFangleYFiltered = 0.0
    oldXAccRawValue = 0
    oldYAccRawValue = 0
    oldZAccRawValue = 0

    a = datetime.datetime.now()



    #Setup the tables for the median filter. Fill them all with '1' so we dont get devide by zero error 
    acc_medianTable1X = [1] * ACC_MEDIANTABLESIZE
    acc_medianTable1Y = [1] * ACC_MEDIANTABLESIZE
    acc_medianTable1Z = [1] * ACC_MEDIANTABLESIZE
    acc_medianTable2X = [1] * ACC_MEDIANTABLESIZE
    acc_medianTable2Y = [1] * ACC_MEDIANTABLESIZE
    acc_medianTable2Z = [1] * ACC_MEDIANTABLESIZE

    IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
    IMU.initIMU()       #Initialise the accelerometer and gyroscope


    while True:
        signal.wait()
        #Read the accelerometer,gyroscope and magnetometer values
        ACCx = IMU.readACCx()
        ACCy = IMU.readACCy()
        ACCz = IMU.readACCz()
        GYRx = IMU.readGYRx()
        GYRy = IMU.readGYRy()
        GYRz = IMU.readGYRz()


        ##Calculate loop Period(LP). How long between Gyro Reads
        b = datetime.datetime.now() - a
        a = datetime.datetime.now()
        LP = b.microseconds/(1000000*1.0)

        ######################################### 
        #### Median filter for accelerometer ####
        #########################################
        # cycle the table
        for x in range (ACC_MEDIANTABLESIZE-1,0,-1 ):
            acc_medianTable1X[x] = acc_medianTable1X[x-1]
            acc_medianTable1Y[x] = acc_medianTable1Y[x-1]
            acc_medianTable1Z[x] = acc_medianTable1Z[x-1]

        # Insert the lates values
        acc_medianTable1X[0] = ACCx
        acc_medianTable1Y[0] = ACCy
        acc_medianTable1Z[0] = ACCz    

        # Copy the tables
        acc_medianTable2X = acc_medianTable1X[:]
        acc_medianTable2Y = acc_medianTable1Y[:]
        acc_medianTable2Z = acc_medianTable1Z[:]

        # Sort table 2
        acc_medianTable2X.sort()
        acc_medianTable2Y.sort()
        acc_medianTable2Z.sort()

        # The middle value is the value we are interested in
        ACCx = acc_medianTable2X[ACC_MEDIANTABLESIZE/2];
        ACCy = acc_medianTable2Y[ACC_MEDIANTABLESIZE/2];
        ACCz = acc_medianTable2Z[ACC_MEDIANTABLESIZE/2];


        #Convert Gyro raw to degrees per second
        rate_gyr_x =  GYRx * G_GAIN
        rate_gyr_y =  GYRy * G_GAIN
        rate_gyr_z =  GYRz * G_GAIN


        #Calculate the angles from the gyro. 
        gyroXangle+=rate_gyr_x*LP
        gyroYangle+=rate_gyr_y*LP
        gyroZangle+=rate_gyr_z*LP

        #Convert Accelerometer values to degrees

        if not IMU_UPSIDE_DOWN:
            # If the IMU is up the correct way (Skull logo facing down), use these calculations
            AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
            AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG
        else:
            #Us these four lines when the IMU is upside down. Skull logo is facing up
            AccXangle =  (math.atan2(-ACCy,-ACCz)*RAD_TO_DEG)
            AccYangle =  (math.atan2(-ACCz,-ACCx)+M_PI)*RAD_TO_DEG



        #Change the rotation value of the accelerometer to -/+ 180 and
        #move the Y axis '0' point to up.  This makes it easier to read.
        if AccYangle > 90:
            AccYangle -= 270.0
        else:
            AccYangle += 90.0



        #Complementary filter used to combine the accelerometer and gyro values.
        CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
        CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle

        ############################ END ##################################
        #Package angles into JSON and output as string
        package = {"y-angle": CFangleX, "z-angle": CFangleY}
        package_string = json.dumps(package)
        
        #Send package over socket
        sensor_socket.sendto(package_string.encode(), ADDRESS)

        #slow program down a bit, makes the output more readable
        time.sleep(0.03)

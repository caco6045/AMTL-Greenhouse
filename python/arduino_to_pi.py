#AMTL - Indoor Greenhouse
#Michael Johnson/Ryan Wood
#This code pulls data from the pin on the arduino that is printing the data that was gathered from the sensors

import serial

def dataPull():

	ser = serial.Serial('COM4',9600)
	print("Connected to: " + ser.portstr)

	floatdata=ser.readline()
	tempdata=ser.readline()
	humdata=ser.readline()
	phdata=ser.readline()
	
	floatdata_i=int(floatdata)
	floatdata_b=bool(floatdata_i)
	tempdata_f=float(tempdata)
	humdata_f=float(humdata)
	phdata_f=float(phdata)
	
	if(floatdata_b==0):
		ser.write("A")
	else:
		ser.write("B")
	
	print(floatdata_b)
	print(tempdata_f)
	print(humdata_f)
	print(phdata_f)
	print

dataPull()

#AMTL - Indoor Greenhouse
#Michael Johnson/Ryan Wood
#This code pulls data from the pin on the arduino that is printing the data that was gathered from the sensors

import serial
	
ser = serial.Serial('COM4',9600)
print("Connected to: " + ser.portstr)

while True:

	floatdata=ser.readline()
	tempdata=ser.readline()
	humdata=ser.readline()
	phdata=ser.readline()
	
	floatdata_i=int(floatdata)
	floatdata_b=bool(floatdata_i)
	floatdata_s=str(floatdata_b)
	
	tempdata_f=float(tempdata)
	tempdata_s=str(tempdata_f)
	
	humdata_f=float(humdata)
	humdata_s=str(humdata_f)
	
	phdata_f=float(phdata)
	phdata_s=str(phdata_f)
	
	f=open("datafile.txt","w")
	f.write(floatdata_s+"\n")
	f.write(tempdata_s+"\n")
	f.write(humdata_s+"\n")
	f.write(phdata_s+"\n")
	
	if(floatdata_b==0):
		ser.write("A")
	else:
		ser.write("B")
	
	print(floatdata_b)
	print(tempdata_f)
	print(humdata_f)
	print(phdata_f)
	print
	f.close()

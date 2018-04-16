#AMTL - Indoor Greenhouse
#Michael Johnson/Ryan Wood
#This code pulls data from the pin on the arduino that is printing the data that was gathered from the sensors

import serial
	
ser = serial.Serial('COM4',9600)
print("Connected to: " + ser.portstr)
prev_plant="none"

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
	
	f_p=open("plant.txt","r")
	plant=f_p.read()
	
	if(prev_plant!=plant):
		if(plant=="Patio Tomato"):
			prev_plant="Patio Tomato"
			ser.write("A")
		
		elif(plant=="Spinach"):
			prev_plant="Spinach"
			ser.write("B")
			
		elif(plant=="Brocolli"):
			prev_plant="Brocolli"
			ser.write("C")
	
	print(floatdata_b)
	print(tempdata_f)
	print(humdata_f)
	print(phdata_f)
	print
	f.close()

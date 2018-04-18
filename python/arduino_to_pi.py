#AMTL - Indoor Greenhouse
#Michael Johnson/Ryan Wood
#This code pulls data from the pin on the arduino that is printing the data that was gathered from the sensors

from time import sleep
import serial
	
#ser = serial.Serial('COM4',9600)
#print("Connected to: " + ser.portstr)
prev_plant="None"
pump_switch=False

while True:
	'''
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
	'''
	f_p=open("plant.txt","r")
	plant_data = []
	for line in f_p:
		plant_data.append(line)
	plant=plant_data[0].rstrip()
	pump_switch=bool(int(plant_data[1]))
	print pump_switch
	f_p.close()
	
	if(prev_plant!=plant):
		if(plant=="Patio Tomato"):
			prev_plant="Patio Tomato"
			#ser.write("A")
		
		elif(plant=="Spinach"):
			prev_plant="Spinach"
			#ser.write("B")
			
		elif(plant=="Brocolli"):
			prev_plant="Brocolli"
			#ser.write("C")
			
	if(pump_switch==True):
		#ser.write("D")
		print "Pump On"
		pump_switch=False
		f_p=open("plant.txt","w")
		f_p.write(plant+"\n")
		f_p.write("0"+"\n")
		print "Pump Off"
		f_p.close()
	'''
	print(floatdata_b)
	print(tempdata_f)
	print(humdata_f)
	print(phdata_f)
	print
	f.close()
	'''
	sleep(2)

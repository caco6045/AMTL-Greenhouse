#AMTL - Indoor Greenhouse
#Michael Johnson/Ryan Wood
#This code pulls data from the pin on the arduino that is printing the data that was gathered from the sensors

from time import sleep
import serial
	
ser = serial.Serial('COM4',9600)#/dev/ttyUSB0',9600)  #different serial ports depending on if running through pi or 
print("Connected to: " + ser.portstr)
prev_plant="None"
pump_switch=False #initialize values

while True:
	floatdata=ser.readline()
	tempdata=ser.readline()  #read sensor values from serial port
	humdata=ser.readline()
	phdata=ser.readline()
	
	#convert to readable numbers/verify reading correct data from serial port
	floatdata_i=int(floatdata)
	floatdata_b=bool(floatdata_i) 
	floatdata_s=str(floatdata_b)
	
	tempdata_f=float(tempdata)
	tempdata_s=str(tempdata_f)
	
	humdata_f=float(humdata)
	humdata_s=str(humdata_f)
	
	phdata_f=float(phdata)
	phdata_s=str(phdata_f)
	
	#write sensor to datafile that touch screen will reference
	f=open("datafile.txt","w")
	f.write(floatdata_s+"\n")
	f.write(tempdata_s+"\n")
	f.write(humdata_s+"\n")
	f.write(phdata_s+"\n")

	#open plant.txt from touch screen and get data from it
	f_p=open("plant.txt","r")
	plant_data = []
	for line in f_p:
		plant_data.append(line)
	plant=plant_data[0].rstrip()  #get plant from file
	pump_switch=bool(int(plant_data[1])) #get whether pump button is on
	f_p.close()
	
	if(prev_plant!=plant): #only alter when plant is changed
		if(plant=="Patio Tomato"):
			prev_plant="Patio Tomato"
			ser.write("A")  #send arduino signal for Patio Tomato
		
		elif(plant=="Spinach"):
			prev_plant="Spinach"
			ser.write("B") #for Spinach
			
		elif(plant=="Brocolli"):
			prev_plant="Brocolli"
			ser.write("C") #for Brocolli
			
	if(pump_switch==True): #if pump button is pressed
		ser.write("D") #send signal to arduino
		print "Pump On"
		pump_switch=False
		f_p=open("plant.txt","w") #open and write to plant.txt turning button off
		f_p.write(plant+"\n")
		f_p.write("0"+"\n")
		print "Pump Off"
		f_p.close()

	print(floatdata_b)
	print(tempdata_f)
	print(humdata_f) #use for debugging
	print(phdata_f)
	print
	f.close()
	#sleep(2)

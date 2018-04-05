#AMTL - Indoor Greenhouse
#Michael Johnson/Ryan Wood
#This code pulls data from the pin on the arduino that is printing the data that was gathered from the sensors

import serial
ser = serial.Serial('COM4',9600)
print("Connected to: " + ser.portstr)

#phrase = []
#flag=True

#ser.write("A")

while True:
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

"""
while flag == True:
	linein=ser.readline()
	#print(linein)
	for line in ser.read():
		phrase.append(chr(line))	#Making a list from the individual bytes from Arduino
		joined_phrase = ''.join(str(p) for p in phrase) #Formats the phrase correctly
		
		if chr(line) == '\r':	#Causes the program to break if the new line character is detected
			flag = False	

print(joined_phrase)
ser.close()
"""

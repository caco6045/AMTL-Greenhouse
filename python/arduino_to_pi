#AMTL - Indoor Greenhouse
#Michael Johnson
#This code pulls data from the pin on the arduino that is printing the data that was gathered from the sensors

import serial
ser = serial.Serial('COM5',9600,timeout=0)
print("Connected to: " + ser.portstr)

phrase = []
flag = True

while flag == True:
	for line in ser.read():
		phrase.append(chr(line))	#Making a list from the individual bytes from Arduino
		joined_phrase = ''.join(str(p) for p in phrase) #Formats the phrase correctly
		
		if chr(line) == '\r':	#Causes the program to break if the new line character is detected
			flag = False	

print(joined_phrase)
ser.close()

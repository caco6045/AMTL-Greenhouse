#AMTL - Indoor Greenhouse
#Michael Johnson/Ryan Wood

from Tkinter import *		#Importing everything from the tkinter library
import datetime				#Importing the datetime library
import serial
import tkMessageBox

root = Tk()		#Define the main window
root.minsize(width=480,height=320)	#Set minimum window size
root.maxsize(width=480,height=320)	#Set maximum window size


plant_options = ["Patio Tomato","Spinach","Brocolli"]	#Define plant options for greenhouse
var = StringVar(root)				 #Define variable var as a string in the main window
var.set(plant_options[0])			 #Set the initial value of var as the first instance in plant_options
p = OptionMenu(root,var,*plant_options)	#Create the option menu in the main window using plant_options
p.grid(row=0,column=0)	#Place the option menu in the main window

def plant_value():					#Pull the current value of the plant
	f_p=open("plant.txt","w")		#Opening a text file with the ability to write to it
	f_p.write(var.get())			#Writing the  plant value to the text file
	f_p.close						#Closing the text file

def confirmation():					#Function to confirm with the user that they want to change the plant value
	ans = tkMessageBox.askquestion("Question 1", "Are you sure you want to update the plant value?") #Creating the message box
	if  ans == "yes":				#Depending on the answer the plant value is either updated or nothing happens
		plant_value()
	elif ans == "no":
		print("no")
	
plant_update = Button(root,text="Update",command=confirmation)	#Create a button to update the plant type
plant_update.grid(row=1,column=0)		#Place the update button in the main window

label_1 = Label(root)				 #Current temperature label	
label_1.grid(row=2,column=0,sticky=W)#Define placement of label and left allign label

label_2 = Label(root)				 #Current humidity label
label_2.grid(row=2,column=1,sticky=E)#Define placement of the label and right allight the label

label_3 = Label(root)				 #Current pH label
label_3.grid(row=3,column=0,sticky=W)#Define placement of label and left allign label

label_4 = Label(root)				 #Current res status label
label_4.grid(row=3,column=1,sticky=E)#Define placement of the label and right allight the label

label_5 = Label(root)				 #Current Time
label_5.grid(row=0,column=1,sticky=E)#Place the "clock"

def dataPull():
	f=open("datafile.txt","r")
	data = []
	for line in f:
		data.append(line)
	temp=data[2]
	hum=data[1]
	pH=data[3]
	res=data[0]			
										#Define the current value of temp
	label_1.configure(text="Temperature: " + temp)		#Configure the temp varialble to be taken as the text argument in  temp Label
	
	label_2.configure(text="Humidity: " + hum)			#Configure the hum varialble to be taken as the text argument in humidity Label	
	
	label_3.configure(text="pH Level: " + pH)			#Configure the pH varialble to be taken as the text argument in pH Label
	
	label_4.configure(text="Reservoir Status: " + res)			#Configure the res varialble to be taken as the text argument in res Label
	root.after(1000,dataPull)		    #Update the res after 1000ms (1sec)
	f.close
	
def clock():
	time = datetime.datetime.now().strftime("Time: %H:%M:%S")
	label_5.config(text=time)
	root.after(1000, clock) 			#Update the clock after 1000 ms (1sec)

dataPull()
clock()									#Run the initial instance of res_update

root.mainloop()

#AMTL - Indoor Greenhouse
#Michael Johnson/Ryan Wood

from Tkinter import *		#Importing everything from the tkinter library
import datetime				#Importing the datetime library
import serial				#Importing pyserial
import tkMessageBox			#Import the messagebox from tkinter
import tkFont
from PIL import Image,ImageTk 	#Importing the necessary image classes from the Python Imaging Library (PIL)
root = Tk()							#Define the main window
#root.minsize(width=480,height=320)	#Set minimum window size
#root.maxsize(width=480,height=320)	#Set maximum window size

helv36 = tkFont.Font(family='Helvetica', size=15, weight='bold')
helv12 = tkFont.Font(family='Helvetica', size=12, weight='bold')
cent20=tkFont.Font(family='Helvetica',size=14,weight='bold')


plant_options = ["Patio Tomato","Spinach","Brocolli"]	#Define plant options for greenhouse
var = StringVar(root)					#Define variable var as a string in the main window
var.set(plant_options[0])			 	#Set the initial value of var as the first instance in plant_options
p = OptionMenu(root,var,*plant_options)	#Create the option menu in the main window using plant_options
p.grid(row=0,column=0,padx=20,pady=5)					#Place the option menu in the main window
p.config(width=12)
p['font']=helv36

image_1 = Image.open("AMTL.png")		#Open the image file
image_1 = image_1.resize((210,60),Image.ANTIALIAS) #Resize the image (w,h)
photo_1 = ImageTk.PhotoImage(image_1)	#Change the image to something tkinter can read
label_p1 = Label(root, image=photo_1)	#Put the image in a label
label_p1.image = photo_1
label_p1.grid(row=6,column=0,sticky=S)			#Place the image in the main window

image_2 = Image.open("dcc-typetreatment-designbuildinvent.png") #Open image file
image_2 = image_2.resize((230,60),Image.ANTIALIAS)	#Resize the image (w,h)
photo_2 = ImageTk.PhotoImage(image_2)	#Change the image to something tkinter can read
label_p2 = Label(root, image=photo_2)	#Put the image in a label
label_p2.image = photo_2
label_p2.grid(row=6,column=1,sticky=S)			#Place the lable in the main window

def plant_value():					#Pull the current value of the plant
	f_p=open("plant.txt","w")		#Opening a text file with the ability to write to it
	f_p.write(var.get()+"\n")		#Writing the  plant value to the text file
	f_p.write("0"+"\n")
	f_p.close						#Closing the text file

def confirmation():					#Function to confirm with the user that they want to change the plant value
	ans = tkMessageBox.askquestion("Confirm", "Are you sure you wish to begin growing a new plant?") #Creating the message box
	if  ans == "yes":				#Depending on the answer the plant value is either updated or nothing happens
		plant_value()
	elif ans == "no":
		print("no")
		
def pump_on():
	f_p=open("plant.txt","w")
	f_p.write(var.get()+"\n")
	f_p.write("1"+"\n")
	f_p.close
	
plant_update = Button(root,text="Update",command=confirmation)	#Create a button to update the plant type
plant_update.grid(row=1,column=0)		#Place the update button in the main window
plant_update.config(width=10)
plant_update['font']=cent20

pump_update = Button(root,text="Pump",command=pump_on)	#Create a button to update the plant type
pump_update.grid(row=0,column=1,sticky=SW,rowspan=2,pady=5)		#Place the update button in the main window
pump_update.config(height=3,width=7)
pump_update['font']=helv36

label_1 = Label(root)				 #Current temperature label	
label_1.grid(row=2,column=0,sticky=W,pady=20)#Define placement of label and left allign label
label_1['font']=cent20

label_2 = Label(root)				 #Current humidity label
label_2.grid(row=2,column=1,pady=20)#Define placement of the label and right allight the label
label_2['font']=cent20

label_3 = Label(root)				 #Current pH label
label_3.grid(row=4,column=0,sticky=W)#Define placement of label and left allign label
label_3['font']=cent20

label_4 = Label(root)				 #Current res status label
label_4.grid(row=4,column=1,pady=20)#Define placement of the label and right allight the label
label_4['font']=cent20

label_5 = Label(root)				 #Current Time
label_5.grid(row=0,column=1,sticky=E,rowspan=2,padx=5)#Place the "clock"
label_5['font']=cent20

def dataPull():
	f=open("datafile.txt","r")
	data = []
	for line in f:
		data.append(line)
	temp=data[2]
	hum=data[1]
	pH=data[3]
	res=data[0]	
	
	if res.rstrip()=="True":
		res_s="Full"
	else:
		res_s="Refill"
										#Define the current value of temp
	label_1.configure(text="Temperature: "+temp.rstrip() +" F")		#Configure the temp varialble to be taken as the text argument in  temp Label
	
	label_2.configure(text="Humidity: "+hum.rstrip()+" %")			#Configure the hum varialble to be taken as the text argument in humidity Label	
	
	label_3.configure(text="pH Level: " + pH)			#Configure the pH varialble to be taken as the text argument in pH Label
	
	if(res_s=="Refill"):
		label_4.configure(text="Reservoir Status: Refill",fg="red")			#Configure the res varialble to be taken as the text argument in res Label
	else:
		label_4.configure(text="Reservoir Status: Full",fg="black")
	
	root.after(1000,dataPull)		    #Update the res after 1000ms (1sec)
	f.close
	
def clock():
	time = datetime.datetime.now().strftime("%I:%M %p")
	label_5.config(text=time)
	root.after(1000, clock) 			#Update the clock after 1000 ms (1sec)

dataPull()
clock()									#Run the initial instance of res_update

root.mainloop()

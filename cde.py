#import xlrd

from tkinter import *
from tkinter.filedialog import askopenfilename

import os

root = Tk()

def printeer(event):
	print("print fn",azi)


def get_file():
	filename = askopenfilename() 			# show an "Open" dialog box and return the path to the selected file
	file= Label(root,text=filename)
	file.grid(row=5,column=1)
	

head= Label(root,text="Landslide model",bg="grey",fg="white")
head.grid(row=0)

label1= Label(root,text="Azimuth :")
label2= Label(root,text="Altitude :")
azi= Entry(root)
alt= Entry(root)


num = azi 


label1.grid(row=1,sticky=E)
label2.grid(row=2,sticky=E)
azi.grid(row=1,column=1)
alt.grid(row=2,column=1)

#adding button
button1 = Button(text="postdtm",fg="red")
path = button1.command(askopenfilename())



button2 = Button(text="predtm",fg="blue",command=get_file)
button1.grid(row=3)
button2.grid(row=3,column=1)


button3 =Button(text="Enter")
button3.grid()

root.mainloop()


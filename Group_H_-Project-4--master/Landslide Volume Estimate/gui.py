from tkinter import *
from tkinter.filedialog import askopenfilename
from gacode import gacode
from tkinter import messagebox
import csv
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap



import os

global ispost
ispost=0
global ispre
ispre=0
global azi
global alt

def stop():
    quit()

def plot(change,cms):
    removal=change>0
    deposit=change<0
    fig, axs = plt.subplots(1,3, figsize=(4, 4), constrained_layout=True)
    axs[0].set_title('Change')
    axs[1].set_title('Removal')
    axs[2].set_title('Deposition')
    psm = axs[0].pcolormesh(change, cmap=cms, rasterized=True, vmin=-100, vmax=100)
    fig.colorbar(psm, ax=axs[0])
    psm = axs[1].pcolormesh(removal, cmap=cms, rasterized=True, vmin=0, vmax=1)
    fig.colorbar(psm, ax=axs[1])
    psm = axs[2].pcolormesh(deposit, cmap=cms, rasterized=True, vmin=0, vmax=1)
    fig.colorbar(psm, ax=axs[2])
    fig.savefig("shapes")
    plt.show()



def get_file_pre():
    filename = askopenfilename()            # show an "Open" dialog box and return the path to the selected file
    file= Label(root,text=filename)
    global pre
    global ispre
    pre = filename
    ispre=1
    file.grid(row=5,column=1)

def get_file_pos():
    filename = askopenfilename()            # show an "Open" dialog box and return the path to the selected file
    file= Label(root,text=filename)
    global post
    global ispost
    post= filename
    ispost=1
    file.grid(row=5,column=1) 

def check_and_execute():
    global azi
    azi=e1.get()
    global alt
    alt=e2.get()
    msg="Dta missing:-\n"
    if ispost==0:
        msg=msg+"PostDTM\n"
    if ispre==0:
        msg=msg+"PreDTM\n"
    if not azi:
        msg=msg+"Azimuth\n"
    if not alt:
        msg=msg+"Altitude\n"
    if ispost==0 or ispre==0 or not azi or not alt:
        messagebox.showerror("Error",msg)
    else:
        if pre.endswith("xlsx") and post.endswith("xlsx"):
            vol,err,change=gacode(post,pre,float(azi),float(alt))
            viridis= cm.get_cmap('viridis',256)
            np.savetxt("change.csv",change,delimiter=",")
            loss= np.transpose(np.where(change>0))
            deposit = np.transpose(np.where(change<0))
            np.savetxt("loss.csv",loss,delimiter=",")
            np.savetxt("deposit.csv",deposit,delimiter=",")
            msg=" Volume of Landslide= "+str(vol)+" cubic meter\n Error="+str(err)+" %\n Resultant images saved \n Data added in data.csv"
            messagebox.showinfo("Result",msg)
            plot(change,viridis)
            
        else:
            msg="PreDTM and PostDTM file should hav xlsx extension"
            messagebox.showerror("Error",msg)

root = Tk()


head= Label(root,text="Landslide model",bg="grey",fg="white")
head.grid(row=0)

label1= Label(root,text="Azimuth :")
label2= Label(root,text="Altitude :")
e1= Entry(root)
e2= Entry(root)


label1.grid(row=1,sticky=E)
label2.grid(row=2,sticky=E)
e1.grid(row=1,column=2)
e2.grid(row=2,column=2)

#adding button
button1 = Button(text="postdtm",fg="red",command=get_file_pos)
#button1.bind("<Button-1>",get_file_pos())



button2 = Button(text="predtm",fg="blue",command=get_file_pre)


button3 = Button(text="Submit",fg="black",command=check_and_execute)

button4 = Button(text="Exit",fg="black",command=stop)
button1.grid(row=3)
button2.grid(row=3,column=1)
button3.grid(row=3,column=2)
button4.grid(row=4,column=1)


root.mainloop()
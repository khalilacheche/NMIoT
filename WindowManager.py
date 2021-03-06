import tkinter as tk
from tkinter import *
from tkinter.filedialog import *
from PIL import ImageTk, Image
from threading import Thread
import os
import sys
class Window ():
    def __init__(self):
        if (os.environ.get('DIPSLAY','') == ''):
            print('no display found')
            os.environ.__setitem__('DISPLAY',':0.0')
        self.numLabels = 6
        self.root = tk.Tk()
        self.root.title("NMIoT")
        self.app=FullScreenApp(self.root)
        self.root.tk_setPalette(background="#FFFFFF")
        self.root.config(cursor="none")
        self.arriving_image= ImageTk.PhotoImage(Image.open("arriving.png").resize((70,70)))
        ####Creating the background
        background_image=ImageTk.PhotoImage(Image.open("back.jpg").resize((self.app.width,self.app.height)))
        background_label = tk.Label(self.root, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image
        ####Creating the frame that will hold the time list
        tlframe = Frame(self.root,borderwidth=1)
        tlframe.pack()
        tlframe.place(height=450,width=400,x=850,y=200)
        ####Creating the time and date labels
        self.localTimeLabel= Label(self.root, text="",font=("Product Sans", 130),fg="#424242", bg="#e8e8e6")
        self.localTimeLabel.place(x=50,y=50)
        self.localDateLabel= Label(self.root, text="",font=("Product Sans", 60),fg="#666666", bg="#e8e8e6")
        self.localDateLabel.place(x=70,y=260)
        ####Creating the timeList labels
        self.timeLabels=[]
        self.directionLabels=[]
        for i in range(0,self.numLabels):
            self.timeLabels.append(Label(tlframe, text="",font=("Product Sans", 50)))
            self.timeLabels[i].grid(row = i, column = 1)
            self.directionLabels.append(Label(tlframe, text="",font=("Product Sans", 20)))
            self.directionLabels[i].grid(row = i, column = 0)
            

        ####Creating the weatherforecast frame
        self.weatherFrame=tk.Frame(self.root, width=700, height=150, borderwidth=1)
        self.weatherFrame.pack()
        self.weatherFrame.place(x=40,y=550)
        #self.weatherFrame["background"]= "#f4f4f4"
        ####Creating the weather cards in the  weatherforecast frame
        self.weatheritems=[]
        for i in range(0,7):
            self.weatheritems.append(weatheritem(self.weatherFrame,i))

    def start (self):
        self.root.wm_attributes('-fullscreen','true')
        self.root.mainloop()

    ############ Update functions definition ############
    def updateDateTime(self,date,time):
        self.localTimeLabel.configure(text=time)
        self.localDateLabel.configure(text=date)
    def updateTimeList(self,timeList):
        for i in range(0,min(len(timeList),self.numLabels)):
            self.directionLabels[i].configure(text= timeList[i].destination+": ")
            if(timeList[i].eta < 1):
                self.timeLabels[i].configure(text= "",image=self.arriving_image)
            else:
                self.timeLabels[i].configure(text=timeList[i].timeStr,fg=timeList[i].color,image = "")
                
    def updateWeatherData(self,data):
        for i in range(0,min(7,len(data))):
            self.weatheritems[i].updateWeatherItem(data[i])



############### Weather item Class definition ###############
class weatheritem:
    def __init__(self,wf,index):#Intializing the card elements in their positions,color etc...
        #colors=["blue","red","green","orange","white","black","purple"]
        self.card=Frame(wf,width=100,height=150,padx=0, pady=0)
        self.card.pack()
        self.card.place(x=100*(index), y=0)
        self.highLabel= Label(self.card, text="",font=("Product Sans", 20),fg="#5f5f5f")
        self.highLabel.place(x=10,y=120)
        self.lowLabel= Label(self.card, text="",font=("Product Sans", 20),fg="#ababab")
        self.lowLabel.place(x=70,y=120)
        self.dayLabel= Label(self.card, text="",font=("Product Sans", 15),fg="#666666")
        self.dayLabel.place(x=35,y=0)
        self.bcg_img=ImageTk.PhotoImage(file="Weather/sun.png")
        self.forecast_label= Label(self.card, text="",font=("Product Sans", 10),fg="#ababab")
        self.forecast_label.place(x=25,y=25)
        self.image_label = tk.Label(self.card, image=self.bcg_img,borderwidth=0,highlightthickness=0)
        self.image_label.place(x=35, y=60)
        self.image_label.image = self.bcg_img

    def updateWeatherItem(self,data):
        self.highLabel.configure(text=data["high"])
        self.lowLabel.configure(text=data["low"])
        self.dayLabel.configure(text=data["day"])
        self.forecast_label.configure(text=data["text"])
        self.bcg_img=ImageTk.PhotoImage(file=weatheritem.getImageByCode(data["code"]))
        self.image_label.configure(image=self.bcg_img)
        self.image_label.image = self.bcg_img#AS seen on stackoverflow, for the agrbage collector
    @staticmethod
    def getImageByCode(code):
        if( code == 26 or code == 28 or code == 30):
            return "Weather/cloudy.png"
        elif (code == 27 or code == 29):
            return "Weather/cloudynight.png"
        elif (code == 8 or code == 9 or code == 18 or code ==20 or code ==21 or code ==22 or code == 23): 
            return "Weather/fog.png"
        elif (code == 40 or code == 35):
            return "Weather/heavyrain.png"
        elif (code == 47 or code == 1 or code == 1 or code == 3 or code == 4 or code == 37 or code == 38):
            return "Weather/lightning.png"
        elif( code == 5 or code == 6 or code == 10 or code == 10 or code == 11 or code == 12 or code == 45):
            return "Weather/rain.png"
        elif (code == 25):
            return "Weather/sdf.png"
        elif (code == 46 or code == 7 or code == 13 or code == 14 or code == 15  or code ==16 or code == 17 or code ==41 or code == 42 or code ==43  or code ==46 ):
            return "Weather/snow.png"
        elif (code == 31 or code == 32 or code == 33 or code == 34 or code ==36):
            return "Weather/sun.png"
        elif( code == 39):
            return "Weather/sunrain.png"
        elif (code == 0 or code == 2 or code == 19 or code == 24):
            return "Weather/wind.png"
        else :
            return "Weather/cloudy.png"


############### FullScreenApp Class definition ###############
class FullScreenApp:
    padding=3
    dimensions="{0}x{1}+0+0"
    def __init__(self, master, **kwargs):
        self.master=master
        self.width=master.winfo_screenwidth()-self.padding
        self.height=master.winfo_screenheight()-self.padding
        master.geometry(self.dimensions.format(self.width, self.height))

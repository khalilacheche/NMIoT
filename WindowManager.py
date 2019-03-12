import tkinter as tk
from tkinter.filedialog import *
from PIL import ImageTk, Image
from threading import Thread

class Window ():
    def __init__(self):
        self.root = tk.Tk()
        self.app=FullScreenApp(self.root)
        ####Creating the background
        background_image=ImageTk.PhotoImage(file="back.jpg")
        background_label = tk.Label(self.root, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image
        ####Creating the frame that will hold the time list
        tlframe = Frame(self.root,borderwidth=1)
        tlframe.pack()
        tlframe.place(height=500,width=400,x=900,y=300)
        ####Creating the time and date labels
        self.localTimeLabel= Label(self.root, text="",font=("Product Sans", 200),fg="#424242", bg="#e8e8e6")
        self.localTimeLabel.place(x=50,y=50)
        self.localDateLabel= Label(self.root, text="",font=("Product Sans", 60),fg="#666666", bg="#e8e8e6")
        self.localDateLabel.place(x=70,y=260)
        ####Creating the timeList labels
        self.labels=[]
        for i in range(0,3):
            self.labels.append(Label(tlframe, text="",font=("Product Sans", 100)))
            self.labels[i].pack()
        ####Creating the weatherforecast frame
        self.weatherFrame=Frame(self.root, width=700, height=150, borderwidth=1)
        self.weatherFrame.pack()
        self.weatherFrame.place(x=62,y=665)
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
        for i in range(0,3):
            self.labels[i].configure(text= timeList[i].value,fg=timeList[i].color)
    def updateWeatherData(self,data):
        for i in range(0,7):
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
        self.dayLabel= Label(self.card, text="",font=("Product Sans", 20),fg="#666666")
        self.dayLabel.place(x=35,y=0)
        self.bcg_img=ImageTk.PhotoImage(file="placeholder.png")
        self.image_label = tk.Label(self.card, image=self.bcg_img,borderwidth=0,highlightthickness=0)
        self.image_label.place(x=35, y=60)
        self.image_label.image = self.bcg_img

    def updateWeatherItem(self,data):
        self.highLabel.configure(text=data["high"])
        self.lowLabel.configure(text=data["low"])
        self.dayLabel.configure(text=data["day"])
        self.bcg_img=ImageTk.PhotoImage(file=weatheritem.getImageByCode(data["code"]))
        self.image_label.configure(image=self.bcg_img)
        self.image_label.image = self.bcg_img#AS seen on stackoverflow, for the agrbage collector
    @staticmethod
    def getImageByCode(code):
        return "placeholder.png"


############### FullScreenApp Class definition ###############
class FullScreenApp:
    padding=3
    dimensions="{0}x{1}+0+0"

    def __init__(self, master, **kwargs):
        self.master=master
        width=master.winfo_screenwidth()-self.padding
        height=master.winfo_screenheight()-self.padding
        master.geometry(self.dimensions.format(width, height))
        #b = tk.Button(self.master, text="Press me!", command=lambda: self.pressed())
        #b.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    #def pressed(self):
    #    print("clicked!")

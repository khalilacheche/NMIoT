import tkinter as tk
from tkinter.filedialog import *
from PIL import ImageTk, Image
from threading import Thread
class Window ():
    def __init__(self):
        self.root = tk.Tk()
        self.app=FullScreenApp(self.root)
        self.labels=[]
        for i in range(0,3):
            self.labels.append(Label(self.root, text="",font=("Helvetica", 100)))

    def start (self):
        self.root.wm_attributes('-fullscreen','true')
        photo = ImageTk.PhotoImage(file="tl.png")
        canvas = Canvas(self.root, width=photo.width(), height=photo.height())
        canvas.create_image(0, 0, anchor=NW, image=photo)
        canvas.pack()
        for mlabel in self.labels:
            mlabel.pack()
        self.root.mainloop()

    def updateTimeList(self,timeList):
        for i in range(0,3):
            self.labels[i].configure(text= timeList[i].value,fg=timeList[i].color)

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

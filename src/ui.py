import tkinter as tk
import os
from tkinter import Frame, Label
from PIL import Image, ImageTk
import pandas as pd

class App:
    def __init__(self, shared_data):

        df_code_map = pd.read_csv("assets/weather/weather_codes.csv",dtype=str)
        self.code_map = df_code_map.to_dict(orient = "records")
        self.code_map = {(x["code"]): x for x in self.code_map}


        self.tl_data = shared_data["tl_data"]
        self.date_data = shared_data["date_data"]
        self.current_weather_data = shared_data["current_weather_data"]
        self.daily_weather_data = shared_data["daily_weather_data"]

        
        self.init_app()
        self.init_tl_frame()
        self.init_date_frame()
        self.init_daily_weather_frame()
        self.init_current_weather_frame()
        # Start the UI update loop
        self.update_ui()
        


    def init_app(self):
        if (os.environ.get('DIPSLAY','') == ''):
            print('no display found')
            os.environ.__setitem__('DISPLAY',':0.0')

        self.root = tk.Tk()
        self.root.title("TLler")
        
        padding=3
        dimensions="{0}x{1}+0+0"
        
        self.width=self.root.winfo_screenwidth()-padding
        self.height=self.root.winfo_screenheight()-padding
        
        self.root.geometry(dimensions.format(self.width, self.height))
        self.root.tk_setPalette(background="#FFFFFF")
        self.root.config(cursor="none")
        self.root.attributes("-fullscreen", True)

        background_image=ImageTk.PhotoImage(Image.open("assets/back.jpg").resize((self.width,self.height)))
        background_label = tk.Label(self.root, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image


    def init_tl_frame(self):
        ####Creating the frame that will hold the time list

        self.last_updated_label = Label(self.root, text="Last updated: ",font=("Product Sans", 15),fg="#666666", bg="white")
        self.last_updated_label.place(x=1000,y=150)

        self.num_rows = 7

        tlframe = Frame(self.root,borderwidth=1)
        tlframe.pack()
        tlframe.place(height=450,width=400,x=850,y=200)
        self.tlframe=tlframe
        self.row_items = []

        for i in range(0,self.num_rows):
            row_item = TLRowItem(parent=tlframe)
            row_item.pack(fill="x", expand=True)
            self.row_items.append(row_item)

    def init_date_frame(self):
        self.localTimeLabel= Label(self.root, text="",font=("Product Sans", 130),fg="#424242", bg="#e8e8e6")
        self.localTimeLabel.place(x=50,y=50)
        self.localDateLabel= Label(self.root, text="",font=("Product Sans", 60),fg="#666666", bg="#e8e8e6")
        self.localDateLabel.place(x=70,y=260)


    def init_daily_weather_frame(self):
        ####Creating the weatherforecast frame
        self.weatherFrame=tk.Frame(self.root, width=700, height=150, borderwidth=1)
        self.weatherFrame.pack()
        self.weatherFrame.place(x=40,y=550)
        self.weatheritems=[]
        for i in range(0,7):
            self.weatheritems.append(WeatherItem(self.weatherFrame,i,self.code_map))
    

    def init_current_weather_frame(self):
        self.current_weather_frame = tk.Frame(self.root, width=200, height=200, borderwidth=1)
        # set background color
        self.current_weather_frame.configure(background="#e8e8e6")
        
        self.current_weather_frame.pack()
        self.current_weather_frame.place(x=40, y=350)
        self.current_weather_card = CurrentWeatherCard(self.current_weather_frame,self.code_map)


        
            


    def update_ui(self):
        """Periodically fetch and display the latest data from the shared list."""
        self.update_tl_frame()
        self.update_date_frame()
        self.update_daily_weather_frame()
        self.update_current_weather_frame()
        self.root.after(2000, self.update_ui)

    def update_tl_frame(self):
        """Update the frame with the latest data."""
        data = self.tl_data.get_data()
        for i, row_item in enumerate(self.row_items):
            if i < len(data):
                row_item.update(data[i])
            else:
                row_item.update(None)
        self.last_updated_label.configure(text=f"Last updated: {pd.Timestamp.now().strftime('%H:%M:%S')}")
    
    def update_date_frame(self):
        data = self.date_data.get_data()
        self.localDateLabel.configure(text=data[0])
        self.localTimeLabel.configure(text=data[1])

    def update_daily_weather_frame(self):
        data = self.daily_weather_data.get_data()

        for i, weather_item in enumerate(self.weatheritems):
            if i < len(data):
                weather_item.update(data[i])
            else:
                weather_item.update(None)

    def update_current_weather_frame(self):
        data = self.current_weather_data.get_data()
        self.current_weather_card.update(data[0])
            



class CurrentWeatherCard(tk.Frame):
    def __init__(self,parent,code_map):
        super().__init__(parent)
        
        
        self.code_map=code_map

        img = Image.open("assets/weather/icons/sunny.png")  # Open image
        img = img.resize((120, 120), Image.LANCZOS)  # Resize image
        weather_icon = ImageTk.PhotoImage(img)

        # Create and place widgets
        self.icon_label = tk.Label(parent, image=weather_icon, borderwidth=0, highlightthickness=0,bg="#e8e8e6")
        self.icon_label.grid(row=0, column=0, rowspan=1, padx=10, pady=10)

        self.temp_label = tk.Label(parent, text="", font=("Product Sans", 60),fg="gray", justify="center",bg="#e8e8e6")
        self.temp_label.grid(row=0, column=1)

        self.description_label = tk.Label(parent, text="", font=("Product Sans", 20), fg="gray", justify="center",bg="#e8e8e6")
        self.description_label.grid(row=1, column=0)

        self.feels_like_label = tk.Label(parent, text="", font=("Product Sans", 20),fg="gray", justify="center",bg="#e8e8e6")
        self.feels_like_label.grid(row=1, column=1, padx=20, sticky="e")

        

    def update(self, current_weather_data):

        if current_weather_data is None:
            self.temp_label.configure(text="")
            self.description_label.configure(text="")
            self.feels_like_label.configure(text="")
            self.icon_label.configure(image="")

            return
        
        temperature = int(current_weather_data["temperature"])
        apparent_temperature = int(current_weather_data["apparent_temperature"])
        
        weather_code = str(int(current_weather_data["weather_code"]))

        code_metadata = self.code_map.get(weather_code, None)

        abbrev = code_metadata["description"] if code_metadata is not None else weather_code
        image_path = f"assets/weather/icons/{code_metadata['image_name']}" if code_metadata is not None else None
        

        # Load and resize image
        
        self.temp_label.configure(text=f"{temperature}°C")
        self.description_label.configure(text=abbrev)
        self.feels_like_label.configure(text=f"Feels like: {apparent_temperature}°C")
        if image_path is not None:
            weather_icon = ImageTk.PhotoImage(Image.open(image_path).resize((120, 120)))
            self.icon_label.configure(image=weather_icon)
            self.icon_label.image = weather_icon
        else:
            self.icon_label.configure(image="")
            self.icon_label.image = None



        



class TLRowItem(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, pady=5)

        # Load and resize image
        
        self.img_label = tk.Label(self)
        self.img_label.pack(side="left", padx=10)

        # Long text label
        self.line_info_label = tk.Label(self, text="", anchor="w", width=20)
        self.line_info_label.pack(side="left", fill="x", expand=True, padx=10)

        # Short text label
        self.eta_label = tk.Label(self, text="", anchor="e", width=30,font=("Product Sans", 30))
        self.eta_label.pack(side="right", padx=10)

    def getTColor(self,eta,color_scale):
        if(eta> color_scale[1]):
            return"#2ecc71"#GREEN
        if (eta> color_scale[0]):
            return "#e67e22"#ORANGE
        return "#e74c3c"#RED
    
    def update(self, departure_item):

        if departure_item is None:
            self.img_label.configure(image="")
            self.img_label.image = None
            self.line_info_label.configure(text="")
            self.eta_label.configure(text="",image="")
            self.eta_label.image = None
            return

        line_metadata = departure_item["metadata"]

        img_path = line_metadata["logo_path"]
        img_width, img_height = line_metadata["logo_size"]

        if img_path is not None:
            img = Image.open(img_path)
            img = img.resize((img_width, img_height), Image.Resampling.LANCZOS)
            self.img = ImageTk.PhotoImage(img)
            self.img_label.configure(image=self.img)
            self.img_label.image = self.img
        else:
            self.img_label.configure(image="")
            self.img_label.image = None
        
        
        # Update the line info label
        
        line_info = f"{departure_item['destination']}"
        self.line_info_label.configure(text=line_info)


        # Update the ETA label

        departure_time = departure_item["departure_time"]
        is_approx = departure_item["is_approx"]
        eta = departure_item["eta"]

        # ETA cutoff represents the time at which we display the time as HH:MM format, rather than " x' ", where x is the number of minutes
        if eta > line_metadata["display_time_cutoff"]: 
            eta_str = departure_time.strftime("%H:%M")
        else:
            eta_str = f"{int(eta)}\'"
        
        if is_approx:
            eta_str = "~" + eta_str

        color = self.getTColor(eta,line_metadata["color_scale"])

        if eta < 1:
            self.eta_label_image = ImageTk.PhotoImage(Image.open("assets/tl/arriving.png").resize((40,40)))
            self.eta_label.config(image=self.eta_label_image,text="         ")
            self.eta_label.image = self.eta_label_image
        else:
            self.eta_label.config(image="",text=eta_str,fg=color)
            self.eta_label.image = None
        

        


class WeatherItem:
    def __init__(self,wf,index,code_map):#Intializing the card elements in their positions,color etc...
        self.code_map=code_map
        self.card=Frame(wf,width=100,height=150,padx=0, pady=0)
        self.card.pack()
        self.card.place(x=100*(index), y=0)
        self.highLabel= Label(self.card, text="",font=("Product Sans", 20),fg="#5f5f5f")
        self.highLabel.place(x=10,y=120)
        self.lowLabel= Label(self.card, text="",font=("Product Sans", 20),fg="#ababab")
        self.lowLabel.place(x=70,y=120)
        self.dayLabel= Label(self.card, text="",font=("Product Sans", 15),fg="#666666")
        self.dayLabel.place(x=35,y=0)
        self.forecast_label= Label(self.card, text="",font=("Product Sans", 10),fg="#ababab")
        self.forecast_label.place(x=25,y=25)
        
        self.image_label = tk.Label(self.card,borderwidth=0,highlightthickness=0)
        self.image_label.place(x=35, y=60)

    def update(self,day_data):
        if day_data is None:
            self.highLabel.configure(text="")
            self.lowLabel.configure(text="")
            self.dayLabel.configure(text="")
            self.forecast_label.configure(text="")
            self.image_label.configure(image="")
            self.image_label.image = None
            return

        min_temp = int(day_data["temp_min"])
        max_temp = int(day_data["temp_max"])
        day = day_data["date"]
        weather_code = str(int(day_data["weather_code"]))

        code_metadata = self.code_map.get(weather_code, None)

        abbrev = code_metadata["description"] if code_metadata is not None else weather_code
        image_path = f"assets/weather/icons/{code_metadata['image_name']}" if code_metadata is not None else None

        self.highLabel.configure(text= f"{max_temp}°")
        self.lowLabel.configure(text= f"{min_temp}°")
        self.dayLabel.configure(text= day)
        self.forecast_label.configure(text=abbrev)
        if image_path is not None:
            self.bcg_img = ImageTk.PhotoImage(Image.open(image_path).resize((50, 50)))

            self.image_label.configure(image=self.bcg_img)
            self.image_label.image = self.bcg_img
        else:
            self.image_label.configure(image="")
            self.image_label.image = None
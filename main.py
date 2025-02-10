from src.tl import TLManager
from src.ui import App
from src.date import DateTimeManager
from src.weather import WeatherManager


def main():
    tl_manager = TLManager("tl_lines_metadata.json")
    tl_manager.start()

    dt_manager = DateTimeManager()
    dt_manager.start()

    weather_manager = WeatherManager()
    weather_manager.start()

    shared_data = {
        "tl_data": tl_manager.upcoming_departures,
        "date_data": dt_manager.date_time,
        "current_weather_data": weather_manager.current_data,
        "daily_weather_data": weather_manager.daily_data
    }

    app = App(shared_data=shared_data)
    app.root.mainloop()
    app.root.after(1000, lambda: app.root.wm_attributes('-fullscreen', 'true'))


if __name__ == "__main__":
    main()
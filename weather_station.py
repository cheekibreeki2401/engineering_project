class Weather_station:
    def __init__(self, weather_station_name, weather_station_location_x, weather_station_location_y, sunlight_exposure,
                 rain_fall, wind_speeds, wind_direction):
        self.weather_station_name = weather_station_name
        self.weather_station_location_x = weather_station_location_x
        self.weather_station_location_y = weather_station_location_y
        self.sunlight_exposure = sunlight_exposure
        self.rain_fall = rain_fall
        self.wind_speeds = wind_speeds
        self.wind_direction = wind_direction

    def get_weather_station_name(self):
        return self.weather_station_name

    def get_weather_station_location_x(self):
        return self.weather_station_location_x

    def get_weather_station_location_y(self):
        return self.weather_station_location_y

    def get_sunlight_exposure(self):
        return self.sunlight_exposure

    def get_rainfall(self):
        return self.rain_fall

    def get_wind_speeds(self):
        return self.wind_speeds

    def get_wind_direction(self):
        return self.wind_direction

class WeatherStation:
    def __init__(self, weather_station_name, weather_station_location_x, weather_station_location_y, local_time, conditions,
                 rain_fall, wind_speeds, temperature, humidity):
        self.weather_station_name = weather_station_name
        self.weather_station_location_x = weather_station_location_x
        self.weather_station_location_y = weather_station_location_y
        self.local_time = local_time
        self.conditions = conditions
        self.rain_fall = rain_fall
        self.wind_speeds = wind_speeds
        self.temperature = temperature
        self.humidity = humidity

    def get_weather_station_name(self):
        return self.weather_station_name

    def get_weather_station_location_x(self):
        return self.weather_station_location_x

    def get_weather_station_location_y(self):
        return self.weather_station_location_y

    def get_local_time(self):
        return self.local_time

    def get_conditions(self):
        return self.conditions

    def get_rainfall(self):
        return self.rain_fall

    def get_wind_speeds(self):
        return self.wind_speeds

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity
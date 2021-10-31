import random
from bs4 import BeautifulSoup as bs
import requests

from WeatherStation import WeatherStation

weather_station_names = ["BRISBANE", "TOWNSVILLE", "CAIRNS"]
weather_station_locations_x = [27.407, 19.259, 16.92]
weather_station_locations_y = [153.02, 146.81, 145.77]


class DatabaseClass:
    def __init__(self):
        self.latest_station_data = []
        self.previous_data = []
        self.closest_station = ""

    # def random_data(self):
    #     for i in range(len(weather_station_names)):
    #         sunlight_data = round(random.uniform(0, 100))
    #         if sunlight_data < 25:
    #             rain_fall = random.randint(61, 300)
    #         elif sunlight_data < 50:
    #             rain_fall = random.randint(21, 60)
    #         else:
    #             rain_fall = random.randint(0, 20)
    #         wind_speed = random.randint(0, 150)
    #         wind_direction_determine = random.randint(0, 7)
    #         switcher = {
    #             0: "North",
    #             1: "North-East",
    #             2: "East",
    #             3: "South-East",
    #             4: "South",
    #             5: "South-West",
    #             6: "West",
    #             7: "North-West"
    #         }
    #         new_temp = round(random.uniform(15, 40))
    #         wind_direction = switcher.get(wind_direction_determine, "No wind")
    #         new_weather_station = WeatherStation(weather_station_names[i], weather_station_locations_x[i],
    #                                               weather_station_locations_x, sunlight_data, rain_fall, wind_speed,
    #                                               wind_direction, new_temp)
    #         self.latest_station_data.append(new_weather_station)

    def get_data(self):
        for i in range(len(weather_station_names)):
            URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
            # place we're searching
            place = weather_station_names[i]
            URL += place
            # get the data
            data = self.get_weather_data(URL)
            # create new weather station and assign recordings
            new_weather_station = WeatherStation(weather_station_names[i], weather_station_locations_x[i], weather_station_locations_x, data["dayhour"], data["weather_now"], data["precipitation"], data["wind"], data["temp_now"], data["humidity"])
            self.latest_station_data.append(new_weather_station)

    def get_weather_data(self, url):  # stores data in a dictionary given a url
        # start a session
        session = requests.Session()

        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                     "(KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"

        LANGUAGE = "en-US,en;q=0.5"

        session.headers['User-Agent'] = USER_AGENT
        session.headers['Accept-Language'] = LANGUAGE
        session.headers['Content-Language'] = LANGUAGE
        html = session.get(url)

        # creates soup object
        soup = bs(html.text, "html.parser")

        # stores results in dictionary
        result = {'region': soup.find("div", attrs={"id": "wob_loc"}).text,
                  'temp_now': soup.find("span", attrs={"id": "wob_tm"}).text,
                  'dayhour': soup.find("div", attrs={"id": "wob_dts"}).text,
                  'weather_now': soup.find("span", attrs={"id": "wob_dc"}).text,
                  'precipitation': soup.find("span", attrs={"id": "wob_pp"}).text,
                  'humidity': soup.find("span", attrs={"id": "wob_hm"}).text,
                  'wind': soup.find("span", attrs={"id": "wob_ws"}).text}

        # get next days weather
        next_days = []
        days = soup.find("div", attrs={"id": "wob_dp"})
        for day in days.findAll("div", attrs={"class": "wob_df"}):
            # gets day name
            day_name = day.findAll("div")[0].attrs['aria-label']
            # gets weather for day
            weather = day.find("img").attrs["alt"]
            temp = day.findAll("span", {"class": "wob_t"})
            # max temp
            max_temp = temp[0].text
            # min temp
            min_temp = temp[2].text
            next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
        # add to result
        result['next_days'] = next_days
        return result

    def get_new_data(self):
        for i in range(len(self.latest_station_data)):
            self.previous_data.insert(0, self.latest_station_data[i])
            if len(self.previous_data) > 100:
                del self.previous_data[100]
        self.latest_station_data = []
        self.get_data()

    def determine_best_location_xy(self, user_x, user_y):
        best_distance = 10000000
        station_name = ""

        for i in range(len(weather_station_names)):
            distance_to_station = (abs(user_y - weather_station_locations_y[i])) / (abs(user_x -
                                                                                        weather_station_locations_x[i]))
            if distance_to_station < best_distance:
                best_distance = distance_to_station
                station_name = weather_station_names[i]
        self.closest_station = station_name

    def determine_best_location_name(self, user_location):
        station_name = ""
        location_match = False
        for i in range(len(weather_station_names)):
            if user_location == weather_station_names[i]:
                station_name = weather_station_names[i]
                self.closest_station = station_name
                location_match = True
        if not location_match:
            return True

    def get_all_current_data(self):
        return self.latest_station_data

    def get_all_archived_data(self):
        return self.previous_data

    def get_all_relevant_current_data(self):
        for data in self.latest_station_data:
            if data.get_weather_station_name() == self.closest_station:
                return data

    def get_all_relevant_archived_data(self):
        data_set = []
        for data in self.previous_data:
            if data.get_weather_station_name() == self.closest_station:
                data_set.append(data)
        return data_set

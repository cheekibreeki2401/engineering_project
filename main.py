import kivy
import requests
import Database

from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime

# https://realpython.com/mobile-app-kivy-python/ provides step by step guide for making an android app from kivy


class WelcomeWindow(Screen):
    # Create instance of database class
    global database1
    database1 = Database.DatabaseClass()

    def on_press_button(self):
        # get location from user
        # if all boxes contain entries
        valid_station = False

        # location name entry
        if self.ids.NameInput.text != '':
            user_location = self.ids.NameInput.text.upper().strip()
            self.ids.NameInput.text = self.ids.NameInput.text.title().strip()
            station = database1.determine_best_location_name(user_location=user_location)
            if not station:
                self.manager.current = 'main'
                valid_station = True
            else:
                self.ids.DescriptionLabel.text = 'Please enter a valid name'
                self.ids.NameInput.text = ''


class MainWindow(Screen):
    def on_enter(self):
        # load data
        self.load_data()

    def load_data(self):
        # based on the current database this will use an x&y input? (or make to have option of name or xy input)

        # select the station to be used (currently returning station name)

        # Get data for this station
        database1.get_new_data()
        records = database1.get_all_relevant_current_data()  # get weather data for nearest location

        # Display the data
        self.ids.TemperatureLabel.text = 'Temperature:' + str(records.get_temperature()) + "C"
        self.ids.TimeLabel.text = 'Time:' + str(records.get_local_time())
        self.ids.SkyLabel.text = 'Condition:' + str(records.get_conditions())
        self.ids.RainLabel.text = 'Rainfall:' + str(records.get_rainfall())
        self.ids.WindLabel.text = 'Wind Speed:' + str(records.get_wind_speeds())
        self.ids.HumidityLabel.text = 'Humidity:' + str(records.get_humidity())


class WindowManager(ScreenManager):
    # make a global kivy accessible variable
    valid_station = False
    pass


# load kivy build file with widgets and layouts
kv = Builder.load_file("screens.kv")


class WeatherLayout(App):

    def build(self):
        return kv

        # Create a screen manager
        # return self.ids.screen_manager


if __name__ == '__main__':
    app = WeatherLayout()
    app.run()

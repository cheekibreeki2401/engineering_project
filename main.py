import kivy
import requests
import Database

# from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from datetime import datetime
from pytz import timezone



# https://realpython.com/mobile-app-kivy-python/ provides step by step guide for making an android app from kivy


class WeatherLayout(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create widgets
        self.SkyLabel = Label(text='Condition:', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .6})
        self.TimeLabel = Label(text='Time', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .7})
        self.RainLabel = Label(text='Rain', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .4})
        self.WindLabel = Label(text='Wind', size_hint=(.2, .2), pos_hint={'center_x': 0.2, 'center_y': .3})
        self.DirectionLabel = Label(text='Wind Direction', size_hint=(.2, .2),
                                    pos_hint={'center_x': 0.65, 'center_y': .3})
        self.TemperatureLabel = Label(text='Temperature:', size_hint=(.2, .2),
                                      pos_hint={'center_x': 0.5, 'center_y': .5})
        self.DescriptionLabel = Label(text='Enter Location:', size_hint=(.1, .1),
                                      pos_hint={'center_x': 0.5, 'center_y': .98})
        # self.UserYInput = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.6, 'center_y': .9})
        # self.UserXInput = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.25, 'center_y': .9})
        self.LocationLabel = Label(text='Location Name:', size_hint=(.2, .2),
                                   pos_hint={'center_x': 0.2, 'center_y': .8})
        self.NameInput = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.5, 'center_y': .8})
        # Create instance of database class
        self.database1 = Database.DatabaseClass()

    def build(self):
        # Create window
        Window.size = (400, 600)
        layout = FloatLayout(size=(350, 250))

        # Add widgets and specify size/position
        button = Button(text='Search',
                        size_hint=(.15, .1),
                        pos_hint={'center_x': 0.85, 'center_y': .9})
        # Set button action
        button.bind(on_press=self.on_press_button)

        # Add widgets to the floating layout
        layout.add_widget(self.DescriptionLabel)
        layout.add_widget(self.LocationLabel)
        layout.add_widget(self.NameInput)
        # layout.add_widget(self.UserXInput)
        # layout.add_widget(self.UserYInput)
        layout.add_widget(button)
        layout.add_widget(self.TemperatureLabel)
        layout.add_widget(self.SkyLabel)
        layout.add_widget(self.TimeLabel)
        layout.add_widget(self.RainLabel)
        layout.add_widget(self.WindLabel)
        layout.add_widget(self.DirectionLabel)

        return layout

    def on_press_button(self, instance):
        # get location from user
        # if all boxes contain entries
        # if (self.UserXInput.text != '' or self.UserYInput.text != '') and self.NameInput.text != '':

        # self.DescriptionLabel.text = 'Please enter an x&y coordinate or Location name'
        # self.UserXInput.text = ''
        # self.UserYInput.text = ''
        # self.NameInput.text = ''

        # location name entry
        if self.NameInput.text != '':
            user_location = self.NameInput.text.upper().strip()
            self.NameInput.text = self.NameInput.text.title().strip()
            station = self.database1.determine_best_location_name(user_location=user_location)
            if not station:
                self.load_data()
            else:
                self.DescriptionLabel.text = 'Please enter a valid name'
                # self.UserXInput.text = ''
                # self.UserYInput.text = ''
                self.NameInput.text = ''
        # xy inputs
        # elif self.UserXInput.text != '' and self.UserYInput.text != '':
            # try:
                # user_x = float(self.UserXInput.text)
                # user_y = float(self.UserYInput.text)
                # self.database1.determine_best_location_xy(user_x=user_x, user_y=user_y)
                # self.load_data()
            # except ValueError:
                # self.DescriptionLabel.text = 'Please enter a valid input'
                # self.UserXInput.text = ''
                # self.UserYInput.text = ''
                # self.NameInput.text = ''
        # any other entry
        # else:
        #     self.DescriptionLabel.text = 'Please enter a valid input'
        #     self.UserXInput.text = ''
        #     self.UserYInput.text = ''
        #     self.NameInput.text = ''

    def load_data(self):
        # insert utilising database here (include error checking etc)
        # based on the current database this will use an x&y input? (or make to have option of name or xy input)

        # select the station to be used (currently returning station name)

        # Get data for this station (no idea if this works(need to review how accessing class data works)
        self.database1.random_data()
        self.database1.get_new_data()  # randomly generating weather data
        records = self.database1.get_all_relevant_current_data()  # get weather data for nearest location

        # Display the data
        self.TemperatureLabel.text = 'Temperature:' + str(records.get_temperature())
        self.TimeLabel.text = 'Time:' + datetime.now().strftime("%H:%M:%S")
        if records.get_sunlight_exposure() < 25:
            sky_condition = " Overcast"
        elif 25 < records.get_sunlight_exposure() < 50:
            sky_condition = " Slightly overcast"
        else:
            sky_condition = " Sunny"

        self.SkyLabel.text = 'Condition:' + sky_condition
        self.RainLabel.text = 'Rainfall:' + str(records.get_rainfall()) + "mm"
        self.WindLabel.text = 'Wind Speed:' + str(records.get_wind_speeds()) + "km/hr"
        self.DirectionLabel.text = 'Wind Direction:' + str(records.get_wind_direction())
    # except :
    #     self.DescriptionLabel.text = 'Error'


if __name__ == '__main__':
    app = WeatherLayout()
    app.run()

import kivy
import requests
import Database_class

from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from datetime import datetime

# https://realpython.com/mobile-app-kivy-python/ provides step by step guide for making an android app from kivy


class WeatherLayout(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create widgets
        self.skylabel = Label(text='Condition:', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .6})
        self.timelabel = Label(text='Time', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .7})
        self.rainlabel = Label(text='Rain', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .4})
        self.windlabel = Label(text='Wind', size_hint=(.2, .2), pos_hint={'center_x': 0.2, 'center_y': .3})
        self.directionlabel = Label(text='Wind Direction', size_hint=(.2, .2), pos_hint={'center_x': 0.65, 'center_y': .3})
        self.temperaturelabel = Label(text='Temperature:', size_hint=(.2, .2),
                                      pos_hint={'center_x': 0.5, 'center_y': .5})
        self.descriptionlabel = Label(text='Enter Location:', size_hint=(.1, .1),
                                      pos_hint={'center_x': 0.2, 'center_y': .98})
        self.usery_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.6, 'center_y': .9})
        self.userx_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.25, 'center_y': .9})
        self.locationlabel = Label(text='Location Name:', size_hint=(.2, .2), pos_hint={'center_x':0.2, 'center_y': .8})
        self.name_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.5, 'center_y': .8})
        # Create instance of database class
        self.database1 = Database_class.DatabaseClass()

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
        layout.add_widget(self.descriptionlabel)
        layout.add_widget(self.locationlabel)
        layout.add_widget(self.name_input)
        layout.add_widget(self.userx_input)
        layout.add_widget(self.usery_input)
        layout.add_widget(button)
        layout.add_widget(self.temperaturelabel)
        layout.add_widget(self.skylabel)
        layout.add_widget(self.timelabel)
        layout.add_widget(self.rainlabel)
        layout.add_widget(self.windlabel)
        layout.add_widget(self.directionlabel)

        return layout

    def on_press_button(self, instance):
        # get location from user
            # if all boxes contain entries
            if (self.userx_input.text != '' or self.usery_input.text != '') and self.name_input.text != '':
                self.descriptionlabel.text = 'Please enter an x&y coordinate or Location name'
                self.userx_input.text = ''
                self.usery_input.text = ''
                self.name_input.text = ''
            # location name entry
            elif self.name_input.text !='':
                userlocation = self.name_input.text
                station = self.database1.determine_best_location_name(user_location=userlocation)
                if not station:
                    self.load_data()
                else:
                    self.descriptionlabel.text = 'Please enter a valid name'
                    self.userx_input.text = ''
                    self.usery_input.text = ''
                    self.name_input.text = ''
            # xy inputs
            elif self.userx_input.text != '' and self.usery_input.text != '':
                try:
                    userx = float(self.userx_input.text)
                    usery = float(self.usery_input.text)
                    self.database1.determine_best_location_xy(user_x=userx, user_y=usery)
                    self.load_data()
                except ValueError:
                    self.descriptionlabel.text = 'Please enter a valid input'
                    self.userx_input.text = ''
                    self.usery_input.text = ''
                    self.name_input.text = ''
            # any other entry
            else:
                self.descriptionlabel.text = 'Please enter a valid input'
                self.userx_input.text = ''
                self.usery_input.text = ''
                self.name_input.text = ''


    def load_data(self):
            # insert utilising database here (include error checking etc)
            # based on the current database this will use an x&y input? (or make to have option of name or xy input)

             # select the station to be used (currently returning station name)

            # Get data for this station (no idea if this works(need to review how accessing class data works)
            self.database1.random_data()  # randomly generating weather data
            records = self.database1.get_all_relevant_current_data()  # get weather data for nearest location

            # Display the data
            self.temperaturelabel.text = 'Temperature:' + str(records.get_temperature())
            self.timelabel.text = 'Time:' + datetime.now().strftime("%H:%M:%S")
            if records.get_sunlight_exposure() < 25:
                sky_condition = " Overcast"
            elif 25 < records.get_sunlight_exposure() < 50:
                sky_condition = " Slightly overcast"
            else:
                sky_condition = " Sunny"

            self.skylabel.text = 'Condition:' + sky_condition
            self.rainlabel.text = 'Rainfall:' + str(records.get_rainfall()) + "mm"
            self.windlabel.text = 'Wind Speed:' + str(records.get_wind_speeds()) + "km/hr"
            self.directionlabel.text = 'Wind Direction:' + str(records.get_wind_direction())
        # except :
        #     self.descriptionlabel.text = 'Error'


if __name__ == '__main__':
    app = WeatherLayout()
    app.run()

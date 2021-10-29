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
    #global valid_station
    #valid_station = False
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #
    #
    #     # Create window
    #     Window.size = (400, 600)
    #
    #     self.ids.DescriptionLabel = Label(text='Enter Location:', size_hint=(.1, .1),
    #                                   pos_hint={'center_x': 0.2, 'center_y': .98})
    #     self.ids.UserYInput = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.6, 'center_y': .9})
    #     self.ids.UserXInput = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.25, 'center_y': .9})
    #     self.ids.locationlabel = Label(text='Location Name:', size_hint=(.2, .2),
    #                                pos_hint={'center_x': 0.2, 'center_y': .8})
    #     self.ids.NameInput = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.5, 'center_y': .8})
    #
    #     # Add widgets and specify size/position
    #     button = Button(text='Search',
    #                     size_hint=(.15, .1),
    #                     pos_hint={'center_x': 0.85, 'center_y': .9})
    #     # Set button action
    #     button.bind(on_press=self.ids.on_press_button)
    #
    #     self.ids.add_widget(self.ids.DescriptionLabel)
    #     self.ids.add_widget(self.ids.locationlabel)
    #     self.ids.add_widget(self.ids.NameInput)
    #     self.ids.add_widget(self.ids.UserXInput)
    #     self.ids.add_widget(self.ids.UserYInput)
    #     self.ids.add_widget(button)


    def on_press_button(self):
        # get location from user
        # if all boxes contain entries
        valid_station = False
        # if (self.ids.UserXInput.text != '' or self.ids.UserYInput.text != '') and self.ids.NameInput.text != '':
        #     self.ids.DescriptionLabel.text = 'Please enter an x&y coordinate or Location name'
        #     self.ids.UserXInput.text = ''
        #     self.ids.UserYInput.text = ''
        #     self.ids.NameInput.text = ''

        # location name entry
        if self.ids.NameInput.text !='':
            user_location = self.ids.NameInput.text.upper()
            station = database1.determine_best_location_name(user_location=user_location)
            if not station:
                # self.ids.load_data()
                self.manager.current = 'main'
                valid_station = True
            else:
                self.ids.DescriptionLabel.text = 'Please enter a valid name'
                # self.ids.UserXInput.text = ''
                # self.ids.UserYInput.text = ''
                self.ids.NameInput.text = ''

        # xy inputs
        # elif self.ids.UserXInput.text != '' and self.ids.UserYInput.text != '':
        #     try:
        #         user_x = float(self.ids.UserXInput.text)
        #         user_y = float(self.ids.UserYInput.text)
        #         database1.determine_best_location_xy(user_x=user_x, user_y=user_y)
        #         valid_station = True
        #         # self.ids.load_data()
        #         self.manager.current = 'main'
        #     except ValueError:  # if the entry is not a valid number
        #         self.ids.DescriptionLabel.text = 'Please enter a valid input'
        #         self.ids.UserXInput.text = ''
        #         self.ids.UserYInput.text = ''
        #         self.ids.NameInput.text = ''
        #
        # # any other entry
        # else:
        #     self.ids.DescriptionLabel.text = 'Please enter a valid input'
        #     self.ids.UserXInput.text = ''
        #     self.ids.UserYInput.text = ''
        #     self.ids.NameInput.text = ''


class MainWindow(Screen):
    def on_enter(self):
        # load data
        self.load_data()

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #
    #     # Create instance of database class
    #     # self.ids.database1 = Database.DatabaseClass()
    #
    #     # Create window
    #     Window.size = (400, 600)
    #     #layout = FloatLayout(size=(350, 250))
    #
    #     # Create widgets
    #     self.ids.SkyLabel = Label(text='Condition:', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .6})
    #     self.ids.TimeLabel = Label(text='Time', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .7})
    #     self.ids.RainLabel = Label(text='Rain', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .4})
    #     self.ids.WindLabel = Label(text='Wind', size_hint=(.2, .2), pos_hint={'center_x': 0.2, 'center_y': .3})
    #     self.ids.directionlabel = Label(text='Wind Direction', size_hint=(.2, .2), pos_hint={'center_x': 0.65, 'center_y': .3})
    #     self.ids.TemperatureLabel = Label(text='Temperature:', size_hint=(.2, .2),
    #                                   pos_hint={'center_x': 0.5, 'center_y': .5})
    #     self.ids.DescriptionLabel = Label(text='Enter Location:', size_hint=(.1, .1),
    #                                   pos_hint={'center_x': 0.2, 'center_y': .98})
    #     self.ids.UserYInput = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.6, 'center_y': .9})
    #     self.ids.UserXInput = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.25, 'center_y': .9})
    #     self.ids.locationlabel = Label(text='Location Name:', size_hint=(.2, .2), pos_hint={'center_x':0.2, 'center_y': .8})
    #     self.ids.NameInput = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.5, 'center_y': .8})

    # Create instance of database class
    # self.ids.database1 = Database.DatabaseClass()

    # Add widgets and specify size/position
    # button = Button(text='Search',
    #                 size_hint=(.15, .1),
    #                 pos_hint={'center_x': 0.85, 'center_y': .9})
    # # Set button action
    # button.bind(on_press=self.ids.on_press_button)

    # # Add widgets to the floating layout
    # self.ids.add_widget(self.ids.DescriptionLabel)
    # self.ids.add_widget(self.ids.locationlabel)
    # self.ids.add_widget(self.ids.NameInput)
    # self.ids.add_widget(self.ids.UserXInput)
    # self.ids.add_widget(self.ids.UserYInput)
    # # self.ids.add_widget(button)
    # self.ids.add_widget(self.ids.TemperatureLabel)
    # self.ids.add_widget(self.ids.SkyLabel)
    # self.ids.add_widget(self.ids.TimeLabel)
    # self.ids.add_widget(self.ids.RainLabel)
    # self.ids.add_widget(self.ids.WindLabel)
    # self.ids.add_widget(self.ids.directionlabel)


    def load_data(self):
        # insert utilising database here (include error checking etc)
        # based on the current database this will use an x&y input? (or make to have option of name or xy input)

        # select the station to be used (currently returning station name)

        # Get data for this station (no idea if this works(need to review how accessing class data works)
        database1.random_data()  # randomly generating weather data
        database1.get_new_data()
        records = database1.get_all_relevant_current_data()  # get weather data for nearest location

        # Display the data
        # self.ids.TemperatureLabel.text = 'Temperature:' + temp
        # self.ids.TimeLabel.text = 'Time:' + time

        #self.ids.SkyLabel.text = 'Condition:' + str(records.get_sunlight_exposure())

        self.ids.TemperatureLabel.text = 'Temperature:' + str(records.get_temperature()) + "C"
        self.ids.TimeLabel.text = 'Time:' + datetime.now().strftime("%H:%M:%S")
        if records.get_sunlight_exposure() < 25:
            sky_condition = " Overcast"
        elif 25 < records.get_sunlight_exposure() < 50:
            sky_condition = " Slightly overcast"
        else:
            sky_condition = " Sunny"

        self.ids.SkyLabel.text = 'Condition:' + sky_condition
        self.ids.RainLabel.text = 'Rainfall:' + str(records.get_rainfall()) + "mm"
        self.ids.WindLabel.text = 'Wind Speed:' + str(records.get_wind_speeds()) + "km/hr"


class WindowManager(ScreenManager):
    valid_station = False
    pass


kv = Builder.load_file("screens.kv")


class WeatherLayout(App):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     # TODO make database1 accessible between each screen
    #     #global database1 = Database.DatabaseClass()

    def build(self):
        return kv

        # Create a screen manager
        # self.ids.screen_manager = ScreenManager()

        # # Welcome Screen
        # self.ids.welcome_page = WelcomeScreen()
        # screen = Screen(name='WelcomeScreen')
        # screen.add_widget(self.ids.welcome_page)
        # self.ids.screen_manager.add_widget(screen)
        #
        # # Main Menu
        # self.ids.main_page = MainScreen()
        # screen = Screen(name='MainMenu')
        # screen.add_widget(self.ids.main_page)
        # self.ids.screen_manager.add_widget(screen)

        return self.ids.screen_manager

if __name__ == '__main__':
    app = WeatherLayout()
    app.run()

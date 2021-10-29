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
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime

# https://realpython.com/mobile-app-kivy-python/ provides step by step guide for making an android app from kivy


class WelcomeWindow(Screen):
    # Create instance of database class
    global database1
    database1 = Database_class.DatabaseClass()
    #global valid_station
    #valid_station = False
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #
    #
    #     # Create window
    #     Window.size = (400, 600)
    #
    #     self.ids.descriptionlabel = Label(text='Enter Location:', size_hint=(.1, .1),
    #                                   pos_hint={'center_x': 0.2, 'center_y': .98})
    #     self.ids.usery_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.6, 'center_y': .9})
    #     self.ids.userx_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.25, 'center_y': .9})
    #     self.ids.locationlabel = Label(text='Location Name:', size_hint=(.2, .2),
    #                                pos_hint={'center_x': 0.2, 'center_y': .8})
    #     self.ids.name_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.5, 'center_y': .8})
    #
    #     # Add widgets and specify size/position
    #     button = Button(text='Search',
    #                     size_hint=(.15, .1),
    #                     pos_hint={'center_x': 0.85, 'center_y': .9})
    #     # Set button action
    #     button.bind(on_press=self.ids.on_press_button)
    #
    #     self.ids.add_widget(self.ids.descriptionlabel)
    #     self.ids.add_widget(self.ids.locationlabel)
    #     self.ids.add_widget(self.ids.name_input)
    #     self.ids.add_widget(self.ids.userx_input)
    #     self.ids.add_widget(self.ids.usery_input)
    #     self.ids.add_widget(button)


    def on_press_button(self):
        # get location from user
        # if all boxes contain entries
        valid_station = False
        if (self.ids.userx_input.text != '' or self.ids.usery_input.text != '') and self.ids.name_input.text != '':
            self.ids.descriptionlabel.text = 'Please enter an x&y coordinate or Location name'
            self.ids.userx_input.text = ''
            self.ids.usery_input.text = ''
            self.ids.name_input.text = ''

        # location name entry
        elif self.ids.name_input.text !='':
            userlocation = self.ids.name_input.text
            station = database1.determine_best_location_name(user_location=userlocation)
            if not station:
                # self.ids.load_data()
                self.manager.current = 'main'
                valid_station = True
            else:
                self.ids.descriptionlabel.text = 'Please enter a valid name'
                self.ids.userx_input.text = ''
                self.ids.usery_input.text = ''
                self.ids.name_input.text = ''

        # xy inputs
        elif self.ids.userx_input.text != '' and self.ids.usery_input.text != '':
            try:
                userx = float(self.ids.userx_input.text)
                usery = float(self.ids.usery_input.text)
                database1.determine_best_location_xy(user_x=userx, user_y=usery)
                valid_station = True
                # self.ids.load_data()
                self.manager.current = 'main'
            except ValueError:  # if the entry is not a valid number
                self.ids.descriptionlabel.text = 'Please enter a valid input'
                self.ids.userx_input.text = ''
                self.ids.usery_input.text = ''
                self.ids.name_input.text = ''

        # any other entry
        else:
            self.ids.descriptionlabel.text = 'Please enter a valid input'
            self.ids.userx_input.text = ''
            self.ids.usery_input.text = ''
            self.ids.name_input.text = ''


class MainWindow(Screen):
    def on_enter(self):
        # load data
        self.load_data()

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #
    #     # Create instance of database class
    #     # self.ids.database1 = Database_class.DatabaseClass()
    #
    #     # Create window
    #     Window.size = (400, 600)
    #     #layout = FloatLayout(size=(350, 250))
    #
    #     # Create widgets
    #     self.ids.skylabel = Label(text='Condition:', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .6})
    #     self.ids.timelabel = Label(text='Time', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .7})
    #     self.ids.rainlabel = Label(text='Rain', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .4})
    #     self.ids.windlabel = Label(text='Wind', size_hint=(.2, .2), pos_hint={'center_x': 0.2, 'center_y': .3})
    #     self.ids.directionlabel = Label(text='Wind Direction', size_hint=(.2, .2), pos_hint={'center_x': 0.65, 'center_y': .3})
    #     self.ids.temperaturelabel = Label(text='Temperature:', size_hint=(.2, .2),
    #                                   pos_hint={'center_x': 0.5, 'center_y': .5})
    #     self.ids.descriptionlabel = Label(text='Enter Location:', size_hint=(.1, .1),
    #                                   pos_hint={'center_x': 0.2, 'center_y': .98})
    #     self.ids.usery_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.6, 'center_y': .9})
    #     self.ids.userx_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.25, 'center_y': .9})
    #     self.ids.locationlabel = Label(text='Location Name:', size_hint=(.2, .2), pos_hint={'center_x':0.2, 'center_y': .8})
    #     self.ids.name_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.5, 'center_y': .8})

    # Create instance of database class
    # self.ids.database1 = Database_class.DatabaseClass()

    # Add widgets and specify size/position
    # button = Button(text='Search',
    #                 size_hint=(.15, .1),
    #                 pos_hint={'center_x': 0.85, 'center_y': .9})
    # # Set button action
    # button.bind(on_press=self.ids.on_press_button)

    # # Add widgets to the floating layout
    # self.ids.add_widget(self.ids.descriptionlabel)
    # self.ids.add_widget(self.ids.locationlabel)
    # self.ids.add_widget(self.ids.name_input)
    # self.ids.add_widget(self.ids.userx_input)
    # self.ids.add_widget(self.ids.usery_input)
    # # self.ids.add_widget(button)
    # self.ids.add_widget(self.ids.temperaturelabel)
    # self.ids.add_widget(self.ids.skylabel)
    # self.ids.add_widget(self.ids.timelabel)
    # self.ids.add_widget(self.ids.rainlabel)
    # self.ids.add_widget(self.ids.windlabel)
    # self.ids.add_widget(self.ids.directionlabel)


    def load_data(self):
        # insert utilising database here (include error checking etc)
        # based on the current database this will use an x&y input? (or make to have option of name or xy input)

        # select the station to be used (currently returning station name)

        # Get data for this station (no idea if this works(need to review how accessing class data works)
        database1.random_data()  # randomly generating weather data
        records = database1.get_all_relevant_current_data()  # get weather data for nearest location

        # Display the data
        # self.ids.temperaturelabel.text = 'Temperature:' + temp
        # self.ids.timelabel.text = 'Time:' + time

        #self.ids.skylabel.text = 'Condition:' + str(records.get_sunlight_exposure())

        self.ids.temperaturelabel.text = 'Temperature:' + str(records.get_temperature()) + "C"
        self.ids.timelabel.text = 'Time:' + datetime.now().strftime("%H:%M:%S")
        if records.get_sunlight_exposure() < 25:
            sky_condition = " Overcast"
        elif 25 < records.get_sunlight_exposure() < 50:
            sky_condition = " Slightly overcast"
        else:
            sky_condition = " Sunny"

        self.ids.skylabel.text = 'Condition:' + sky_condition
        self.ids.rainlabel.text = 'Rainfall:' + str(records.get_rainfall()) + "mm"
        self.ids.windlabel.text = 'Wind Speed:' + str(records.get_wind_speeds()) + "km/hr"


class WindowManager(ScreenManager):
    valid_station = False
    pass


kv = Builder.load_file("screens.kv")


class WeatherLayout(App):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     # TODO make database1 accessible between each screen
    #     #global database1 = Database_class.DatabaseClass()

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

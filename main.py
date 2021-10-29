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

# https://realpython.com/mobile-app-kivy-python/ provides step by step guide for making an android app from kivy



class WeatherLayout(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # TODO make database1 accessible between each screen
        #global database1 = Database_class.DatabaseClass()

    def build(self):
        # Create a screen manager
        self.screen_manager = ScreenManager()

        # Welcome Screen
        self.welcome_page = WelcomeScreen()
        screen = Screen(name='WelcomeScreen')
        screen.add_widget(self.welcome_page)
        self.screen_manager.add_widget(screen)

        # Main Menu
        self.main_page = MainScreen()
        screen = Screen(name='MainMenu')
        screen.add_widget(self.main_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

class WelcomeScreen(FloatLayout):
    # Create instance of database class
    global database1
    database1 = Database_class.DatabaseClass()
    global valid_station
    valid_station = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        # Create window
        Window.size = (400, 600)

        self.descriptionlabel = Label(text='Enter Location:', size_hint=(.1, .1),
                                      pos_hint={'center_x': 0.2, 'center_y': .98})
        self.usery_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.6, 'center_y': .9})
        self.userx_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.25, 'center_y': .9})
        self.locationlabel = Label(text='Location Name:', size_hint=(.2, .2),
                                   pos_hint={'center_x': 0.2, 'center_y': .8})
        self.name_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.5, 'center_y': .8})

        # Add widgets and specify size/position
        button = Button(text='Search',
                        size_hint=(.15, .1),
                        pos_hint={'center_x': 0.85, 'center_y': .9})
        # Set button action
        button.bind(on_press=self.on_press_button)

        self.add_widget(self.descriptionlabel)
        self.add_widget(self.locationlabel)
        self.add_widget(self.name_input)
        self.add_widget(self.userx_input)
        self.add_widget(self.usery_input)
        self.add_widget(button)


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
                station = database1.determine_best_location_name(user_location=userlocation)
                if not station:
                    # self.load_data()
                    app.screen_manager.current = 'MainMenu'
                    valid_station = True
                else:
                    self.descriptionlabel.text = 'Please enter a valid name'
                    self.userx_input.text = ''
                    self.usery_input.text = ''
                    self.name_input.text = ''

            # xy inputs
            elif self.userx_input.text != '' and self.usery_input.text != '':
                try:
                    userx = int(self.userx_input.text)
                    usery = int(self.usery_input.text)
                    database1.determine_best_location_xy(user_x=userx, user_y=usery)
                    valid_station = True
                    # self.load_data()
                    app.screen_manager.current = 'MainMenu'
                except ValueError:  # if the entry is not a valid number
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



class MainScreen(FloatLayout):
    def on_enter(self):
        # load data
        self.load_data()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create instance of database class
        # self.database1 = Database_class.DatabaseClass()

        # Create window
        Window.size = (400, 600)
        #layout = FloatLayout(size=(350, 250))

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
        # self.database1 = Database_class.DatabaseClass()

        # Add widgets and specify size/position
        # button = Button(text='Search',
        #                 size_hint=(.15, .1),
        #                 pos_hint={'center_x': 0.85, 'center_y': .9})
        # # Set button action
        # button.bind(on_press=self.on_press_button)

        # Add widgets to the floating layout
        self.add_widget(self.descriptionlabel)
        self.add_widget(self.locationlabel)
        self.add_widget(self.name_input)
        self.add_widget(self.userx_input)
        self.add_widget(self.usery_input)
        # self.add_widget(button)
        self.add_widget(self.temperaturelabel)
        self.add_widget(self.skylabel)
        self.add_widget(self.timelabel)
        self.add_widget(self.rainlabel)
        self.add_widget(self.windlabel)
        self.add_widget(self.directionlabel)


    def load_data(self):
            # insert utilising database here (include error checking etc)
            # based on the current database this will use an x&y input? (or make to have option of name or xy input)

             # select the station to be used (currently returning station name)

            # Get data for this station (no idea if this works(need to review how accessing class data works)
            database1.random_data()  # randomly generating weather data
            records = database1.get_all_relevant_current_data()  # get weather data for nearest location

            # Display the data
            # self.temperaturelabel.text = 'Temperature:' + temp
            # self.timelabel.text = 'Time:' + time

            self.skylabel.text = 'Condition:' + str(records.get_sunlight_exposure())
            self.rainlabel.text = 'Rainfall:' + str(records.get_rainfall())
            self.windlabel.text = 'Wind Speed:' + str(records.get_wind_speeds())
            self.directionlabel.text = 'Wind Direction:' + str(records.get_wind_direction())



if __name__ == '__main__':
    app = WeatherLayout()
    app.run()

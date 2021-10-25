import kivy
import requests

from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

# https://realpython.com/mobile-app-kivy-python/ provides step by step guide for making an android app from kivy
import Database_class

database = Database_class


class WeatherLayout(App):
    # create an instance of the database class for use here

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skylabel = Label(text='Condition:', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .6})
        self.timelabel = Label(text='Time', size_hint=(.2, .2), pos_hint={'center_x': 0.5, 'center_y': .7})
        self.temperaturelabel = Label(text='Temperature:', size_hint=(.2, .2),
                                      pos_hint={'center_x': 0.5, 'center_y': .5})
        self.descriptionlabel = Label(text='Enter Location:', size_hint=(.1, .1),
                                      pos_hint={'center_x': 0.2, 'center_y': .9})
        self.usery_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.6, 'center_y': .9})
        self.userx_input = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.2, 'center_y': .9})
        self.textbox = TextInput(size_hint=(.3, .1), pos_hint={'center_x': 0.5, 'center_y': .9})

    def build(self):
        # Create window
        Window.size = (400, 600)
        layout = FloatLayout(size=(350, 250))

        # Add widgets and specify size/position
        button = Button(text='Search',
                        size_hint=(.15, .1),
                        pos_hint={'center_x': 0.75, 'center_y': .9})
        # Set button action
        button.bind(on_press=self.on_press_button)

        # Add widgets to the floating layout
        layout.add_widget(self.descriptionlabel)
        layout.add_widget(self.textbox)
        layout.add_widget(button)
        layout.add_widget(self.temperaturelabel)
        layout.add_widget(self.skylabel)
        layout.add_widget(self.timelabel)

        return layout

    def on_press_button(self, instance):
        # get location name from
        # city = self.textbox.text
        user_x = self.userx_input.text
        user_y = self.usery_input.text

        # insert utilising database here (include error checking etc)
        # based on the current database this will use an x&y input? (or make to have option of name or xy input)

        # select the station to be used (currently returning station name)
        # station = Database_class.Database_class.determine_best_location(user_x=user_x, user_y=user_y)
        station = database.Database_class.determine_best_location(user_x=user_x, user_y=user_y)

        # get data for this station (no idea if this works(need to review how accessing class data works)
        Database_class.Database_class.get_all_current_data()

        # maybe have the database be updated and then we access it

        # display the data
        self.temperaturelabel.text = 'Temperature:' + temp
        self.timelabel.text = 'Time:' + time
        self.skylabel.text = 'Condition:' + sky


if __name__ == '__main__':
    app = WeatherLayout()
    app.run()

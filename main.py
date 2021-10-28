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
        # get location name from
        # city = self.textbox.text
        #TODO error checking. Make only valid input. Change to location entry
        userx = int(self.userx_input.text)
        usery = int(self.usery_input.text)

        # insert utilising database here (include error checking etc)
        # based on the current database this will use an x&y input? (or make to have option of name or xy input)


        # Create instance of database class
        database1 = Database_class.DatabaseClass()
        # select the station to be used (currently returning station name)
        station = database1.determine_best_location(user_x=userx, user_y=usery)

        # get data for this station (no idea if this works(need to review how accessing class data works)
        database1.random_data()  #randomly generating weather data
        records = database1.get_all_relevant_current_data() #get weather data for nearest location

        # display the data
        #elf.temperaturelabel.text = 'Temperature:' + temp
        #self.timelabel.text = 'Time:' + time

        self.skylabel.text = 'Condition:' + str(records.get_sunlight_exposure())
        self.rainlabel.text = 'Rainfall:' + str(records.get_rainfall())
        self.windlabel.text = 'Wind Speed:' + str(records.get_wind_speeds())
        self.directionlabel.text = 'Wind Direction:' + str(records.get_wind_direction())


if __name__ == '__main__':
    app = WeatherLayout()
    app.run()

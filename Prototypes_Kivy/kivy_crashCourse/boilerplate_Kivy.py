import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty

import random

# APP SOURCE: https://github.com/kivy/kivy/blob/master/kivy/app.py
# WIDGETS: https://kivy.org/doc/stable/api-kivy.uix.html
# CRASH COURSE: http://inclem.net/pages/kivy-crash-course/


class ScatterTextWidget(BoxLayout):
    text_colour = ObjectProperty([1, 0, 0, 1])

    def change_label_colour(self, *args):
        colour = [random.random() for i in range(3)] + [1]
        self.text_colour = colour

class App(App):
    def build(self):
        return ScatterTextWidget()


if __name__ == '__main__':
    App().run()

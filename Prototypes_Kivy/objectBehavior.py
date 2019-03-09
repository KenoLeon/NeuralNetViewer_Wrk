

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.app import App
from kivy.graphics import Color, Rectangle, Canvas
from random import random as r
from functools import partial


# object objectBehaviorApp
# add objects to a canvas or Widget

class FocusButton(FocusBehavior, Button):
      pass
      
class objectBehaviorApp(App):

    def build(self):
        grid = GridLayout(cols=4)
        for i in range(40):
            grid.add_widget(FocusButton(text=str(i)))
        return grid

if __name__ == '__main__':
    objectBehaviorApp().run()

#!/usr/bin/env python

"""
NNV - wip 002 :
Layout + canvas

To Do:

learn Kivy :
- Canvas Animations

wip 003 :
-Grid

"""


from kivy.app import App
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from random import random as r


# Window :
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')


class rootCanvas(Widget):
    def __init__(self, **kwargs):
        super(rootCanvas, self).__init__(**kwargs)
        with self.canvas:
            Color(0.4, 0.4, 0.4, mode='rgb')
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.size[0], self.size[1])

    def play_stop(self, *args):
        print ('will play_stop')

class wip002(App):
    def build(self):
        root = BoxLayout()
        sideBar = BoxLayout(
            padding = 4,
            orientation ='vertical',
            size_hint=(None, 1),
            width = 200,
            spacing = 2)
        widget = rootCanvas()
        root.add_widget(widget)
        btn_1 = Button(
            text='Play/Pause',
            background_normal= '',
            background_color= (.2, .2, .2, 1),
            color = (.6, .6, .6, 1),
            size_hint =(None, None),
            width = 192,
            height = 40,
            on_press=widget.play_stop)

        btn_2 = Button(
            text='Play/Pause',
            background_normal= '',
            background_color= (.2, .2, .2, 1),
            color = (.6, .6, .6, 1),
            size_hint =(None, None),
            width = 192,
            height = 40,
            on_press=widget.play_stop)

        btn_3 = Button(
            text='Play/Pause',
            background_normal= '',
            background_color= (.2, .2, .2, 1),
            color = (.6, .6, .6, 1),
            size_hint =(None, None),
            width = 192,
            height = 40,
            on_press=widget.play_stop)

        btn_4 = Button(
            text='Play/Pause',
            background_normal= '',
            background_color= (.2, .2, .2, 1),
            color = (.6, .6, .6, 1),
            size_hint =(None, None),
            width = 192,
            height = 40,
            on_press=widget.play_stop)

        sideBar.add_widget(btn_1)
        sideBar.add_widget(btn_2)
        sideBar.add_widget(btn_3)
        sideBar.add_widget(btn_4)
        sideBar.add_widget(Widget())

        root.add_widget(sideBar)
        return root


if __name__ == '__main__':
    wip002().run()

#!/usr/bin/env python
"""
NNV - wip 003 :
Layout + canvas

To Do:
Grid Background on Canvas
canvas Animation

"""

from kivy.app import App
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.config import Config
from random import random as r

# Window :
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')


class rootCanvas(Widget):
    def __init__(self, **kwargs):
        super(rootCanvas, self).__init__(**kwargs)
        with self.canvas:
            Color(0.1, 0.1, 0.1, mode='rgb')
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.size[0], self.size[1])

    def play_stop(self, *args):
        print('will play_stop')


class wip003(App):
    def build(self):
        root = BoxLayout()
        sideBar = BoxLayout(
            padding=4,
            orientation='vertical',
            size_hint=(None, 1),
            width=200,
            spacing=2)
        widget = rootCanvas()
        root.add_widget(widget)

        multi_btn_1 = GridLayout(cols=4)
        mb1Label_1 = Label(
        color = (0.6,0.6,0.6,1),
        text='  Grid Size:',
        font_size = 14,
        size_hint =(None, None),
        height = 40
         )
        btn_1 = Button(
            text='-',
            background_normal= '',
            background_color= (.2, .2, .2, 1),
            color = (.6, .6, .6, 1),
            size_hint =(.25, None),
            height = 40,
            on_press=widget.play_stop)
        mb1Label_2 = Label(
        color = (0.6,0.6,0.6,1),
        text='100',
        font_size = 14,
        size_hint =(.25, None),
        height = 40,
         )
        btn_2 = Button(
            text='+',
            background_normal= '',
            background_color= (.2, .2, .2, 1),
            color = (.6, .6, .6, 1),
            size_hint =(.25, None),
            height = 40,
            on_press=widget.play_stop)
        multi_btn_1.add_widget(mb1Label_1)
        multi_btn_1.add_widget(btn_1)
        multi_btn_1.add_widget(mb1Label_2)
        multi_btn_1.add_widget(btn_2)
        sideBar.add_widget(multi_btn_1)
        sideBar.add_widget(Widget())
        root.add_widget(sideBar)
        return root


if __name__ == '__main__':
    wip003().run()

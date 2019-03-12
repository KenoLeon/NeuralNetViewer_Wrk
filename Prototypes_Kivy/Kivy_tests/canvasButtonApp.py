

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Color, Rectangle, Canvas
from random import random as r
from functools import partial


class canvasButtonApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')
        widget = Widget(size_hint=(1, 1))
        layout.add_widget(widget)
        with widget.canvas:
            Color(0.6,0.6,0.6, mode='rgb')
            Rectangle()
        return layout

if __name__ == '__main__':
    canvasButtonApp().run()



    # rootLayout = BoxLayout()
    # left_box = BoxLayout(size = rootLayout.size)
    # right_box = BoxLayout(size = rootLayout.size)
    # # widget = Widget()
    # # left_box.add_widget(widget)
    # with left_box.canvas:
    #     Color(0.6,0.6,0.6, mode='rgb')
    #     Rectangle(size = rootLayout.size)
    # with right_box.canvas:
    #     Color(0.6,0.6,0.6, mode='rgb')
    #     Rectangle(size = rootLayout.size)
    #
    # rootLayout.add_widget(left_box)
    # rootLayout.add_widget(right_box)
    # return rootLayout

        #
        # boxLayout = BoxLayout(width = 200)
        # btn_1 = Button(text='buton_1',
        #                     on_press=partial(self.update, widget))
        #
        # boxLayout.add_widget(btn_1)
        # rootLayout.add_widget(boxLayout)
        #
        # widget.width = widget.width - boxLayout.width

    # def update(self, wid, *largs):
    #     wid.canvas.clear()
    #     with wid.canvas:
    #         Color(r(), 1, 1, mode='hsv')
    #         Rectangle()

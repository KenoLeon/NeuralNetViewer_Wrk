import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

# import random

# APP SOURCE: https://github.com/kivy/kivy/blob/master/kivy/app.py
# WIDGETS: https://kivy.org/doc/stable/api-kivy.uix.html
# CRASH COURSE: http://inclem.net/pages/kivy-crash-course/

# class App(App):
#     def build(self):
#         b = BoxLayout(orientation='vertical')
#         t = TextInput(text='default',
#               font_size=150,
#               size_hint_y=None,
#               height=200)
#         f = FloatLayout()
#         s = Scatter()
#         l = Label(text='moving', font_size=150)
#         f.add_widget(s)
#         s.add_widget(l)
#         b.add_widget(t)
#         b.add_widget(f)
#         t.bind(text=l.setter('text'))
#         return b


class ScatterTextWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(ScatterTextWidget, self).__init__(**kwargs)

        with self.canvas:
            Color(0, 1, 0, 1)
            Rectangle(pos=(0, 100), size=(300, 100))
            Ellipse(pos =(0, 400), size=(300, 100))
            Line(points=[0, 0, 500, 600, 400, 300], close=True, width=3)
    # def change_label_colour(self, *args):
    #     colour = [random.random() for i in range(3)] + [1]
    #     label = self.ids['my_label']
    #     label.color = colour


class App(App):
    def build(self):
        return ScatterTextWidget()


if __name__ == '__main__':
    App().run()

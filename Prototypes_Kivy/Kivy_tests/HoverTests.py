import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget




class target(Widget):
    pass


class HoverTests(App):

    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    HoverTests().run()

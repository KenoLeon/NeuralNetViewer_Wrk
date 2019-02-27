# canvasCallApp.py...

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *

class RootLayout(BoxLayout):
    pass

class canvasCallApp(App):
    def build(self):
        root = RootLayout()
        return RootLayout()

    def update(self):
        pass

if __name__ == '__main__':
    canvasCallApp().run()

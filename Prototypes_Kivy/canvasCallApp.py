# canvasCallApp.py...

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *

class RootLayout(BoxLayout):
    def update(self):
        print('updating')
        # with self.canvas:
        #     Color(0.1, 0.1, 0.1)

class canvasCallApp(App):

    def build(self):
        root = RootLayout()
        return RootLayout()


if __name__ == '__main__':
    canvasCallApp().run()

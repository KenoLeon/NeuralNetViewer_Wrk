from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Canvas

class RootLayout(BoxLayout):
    def __init__(self, **kwargs):
        self.canvas = Canvas()
        with self.canvas:
            Color(0.6, 0.6, 0.6)

class rootLayoutApp(App):
    def build(self):
        root = RootLayout()
        return root


if __name__ == '__main__':
    rootLayoutApp().run()

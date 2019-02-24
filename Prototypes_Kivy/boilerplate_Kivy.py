import kivy
from kivy.app import App
# from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.config import Config


# https://kivy.org/doc/stable/api-kivy.uix.layout.html#kivy.uix.layout.Layout

# Window :
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

class boilerPlateApp(App):
    def build(self):
        layout = BoxLayout()
        # btn1 = Button(text='Button 1 ')
        # btn2 = Button(text='Button 2')
        # layout.add_widget(btn1)
        # layout.add_widget(btn2)
        return layout

if __name__ == '__main__':
    boilerPlateApp().run()

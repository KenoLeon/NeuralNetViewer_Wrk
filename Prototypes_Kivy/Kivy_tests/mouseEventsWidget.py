from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Line, Ellipse, Rectangle

Window.set_system_cursor('crosshair')

class MousePosDemo(BoxLayout):

    def __init__(self, **kwargs):
        super(MousePosDemo, self).__init__(**kwargs)

        Window.bind(mouse_pos=self.mouse_pos)
        # Window.bind(on_motion=self.on_motion)

        self.bind(pos=self.draw)
        self.bind(size=self.draw)
        self.layout1 = BoxLayout(opacity=1)
        self.label = Label()
        self.add_widget(self.layout1)
        self.add_widget(self.label)

    def draw(self, *args):

        self.layout1.canvas.clear()
        with self.canvas.before:
            Color(0.6, 0.6, 0.6, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)

    def mouse_pos(self, window, pos):
        self.label.text = str(pos)

    # def on_motion(self, obj, etype, me):
    #     pass
    #     # self.label.text = str(me.pos)

    def on_touch_down(self, event):
        self.label.text = "touch DOWN: " + str(event.pos)

    def on_touch_up(self, event):
        self.label.text = "touch UP: " + str(event.pos)


class TestApp(App):
    title = "Kivy Mouse Pos Demo"

    def build(self):
        return MousePosDemo()


if __name__ == "__main__":
    TestApp().run()

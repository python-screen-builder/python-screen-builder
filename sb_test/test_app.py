from gui import *
from kivy.app import App
from widget_screen import WidgetScreen

class TestScreen(WidgetScreen):

    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.load_screen()

class TestApp(App):

    def build(self):
        Window.clearcolor = 'steelblue'
        self.test_screen = TestScreen(file_name = 'test_button.json')
        self.test_screen.button1.bind(on_press = self.on_press)
        return self.test_screen

    def on_press(self, button):
        print("button, button, you pressed the button!")
        pass
    
if __name__ == '__main__':
    TestApp().run()

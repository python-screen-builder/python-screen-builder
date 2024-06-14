from gui import *
from kivy.app import App
from widget_screen import WidgetScreen

#global test_screen

class TestScreen(WidgetScreen):

    def __init__(self, **kwargs):
        screen = kwargs.get('screen')
        super(TestScreen, self).__init__(**kwargs)
        self.screen = screen
        self.load_screen()
        self.button1.bind(on_press = self.on_press)

    def on_press(self, button):
        print("Button, button - you clicked the button!")
        pass

class TestApp(App):

    def build(self):
        Window.clearcolor = 'steelblue'
        screen = Screen(name = "Test")
        self.test_screen = TestScreen(file_name = 'test_button.json', screen = screen)
        return screen

if __name__ == '__main__':
    TestApp().run()

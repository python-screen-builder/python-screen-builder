from gui import *
from kivy.app import App
from widget_screen import WidgetScreen

global test_screen

class TestWidgets(WidgetScreen):

    def __init__(self, **kwargs):
        screen = kwargs.get('screen')
        super(TestWidgets, self).__init__(**kwargs)
        self.screen = screen
        self.load_screen()

class TestApp(App):

    def build(self):
        Window.clearcolor = 'steelblue'
        screen = Screen(name = "Test")
        self.test_screen = TestWidgets(file_name = 'test_button.json', screen = screen)
        return screen

if __name__ == '__main__':
    TestApp().run()

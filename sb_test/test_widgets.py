from gui import *
from kivy.app import App
from widget_container import WidgetContainer

class TestScreen(WidgetContainer):

    def __init__(self, **kwargs):
        self.screen = kwargs.get('screen')
        self.file_name = kwargs.get('file_name')
        super(TestScreen, self).__init__(**kwargs)
        self.load_screen()

class TestApp(App):

    def build(self):
        Window.clearcolor = 'steelblue'
        main_layout = BoxLayout(orientation = "vertical")
        menu = Menu(pos_hint = { 'top': 1 })
        menu.add_item(MenuButton(text = "File"))#, on_press = self.on_file))
        main_layout.add_widget(menu)
        self.screen = Screen(name = "test")
        self.test_screen = TestScreen(file_name = 'test_widgets.json', menu_height = 100, screen = self.screen)
        self.test_screen.list.values = [ "apple", "peaches", "pumpkin", "pie" ]
        self.test_screen.list.bind(text = self.on_select)
        self.test_screen.slider.bind(value = self.on_slider)
        self.test_screen.knob1.value = 30
        self.test_screen.knob2.value = 70
        self.test_screen.knob1.bind(value = self.on_knob)
        self.test_screen.knob2.bind(value = self.on_knob)
        self.test_screen.toggle1.bind(on_press = self.on_toggle)
        self.test_screen.text1.bind(text = self.on_change)
        self.test_screen.switch1.active = True
        self.test_screen.switch1.bind(active = self.on_switch)
        for key in self.test_screen.piano.midi_notes:
            if key == None: continue
            key.bind(on_press = self.on_key)
        main_layout.add_widget(self.screen)
        return main_layout

    def on_select(self, instance, value):
        print(value)

    def on_slider(self, instance, value):
        print(value)

    def on_knob(self, instance, value):
        print(value)

    def on_change(self, instance, value):
        print(value)

    def on_switch(self, instance, value):
        print(value)

    def on_toggle(self, instance):
        pass

    def on_key(self, button):
        print(button.id)

if __name__ == '__main__':
    TestApp().run()

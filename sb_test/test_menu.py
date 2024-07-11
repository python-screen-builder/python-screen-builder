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
        self.screen_manager = ScreenManager()
        main_layout = BoxLayout(orientation = "vertical")
        menu = Menu(pos_hint = { 'top': 1 })
        file_menu = SubMenu(text = 'File', values = [ 'Save', 'Load', 'Exit' ])
        help_menu = SubMenu(text = 'Help', values = [ 'About' ])
        file_menu.handler = self.on_file
        help_menu.handler = self.on_help
        menu.add_item(file_menu)
        menu.add_item(MenuButton(text = "screen1", on_press = self.on_menu))
        menu.add_item(MenuButton(text = "screen2", on_press = self.on_menu))
        menu.add_item(MenuButton(text = "screen3", on_press = self.on_menu))
        menu.add_item(help_menu)
        main_layout.add_widget(menu)
        main_layout.add_widget(self.screen_manager)
        self.screen1 = TestScreen(name = 'screen1', file_name = 'test_button.json', menu_height = 100)
        self.screen2 = TestScreen(name = 'screen2', file_name = 'test_widgets.json', menu_height = 100)
        self.screen3 = TestScreen(name = 'screen3', file_name = 'test_panel.json', menu_height = 100)
        self.screen_manager.add_widget(self.screen1)
        self.screen_manager.add_widget(self.screen2)
        self.screen_manager.add_widget(self.screen3)
        self.screen_manager.current = 'screen1'
        return main_layout

    def on_file(self, button):
        pass

    def on_menu(self, button):
        self.screen_manager.current = button.text

    def on_help(self, button):
        title = "About"
        if button.text != 'About': return
        message = Label(text = "Test Menu App", size_hint = (1, 1))
        mb = MessageBox(title = title, message = message, size = (400, 400))
        mb.open()

if __name__ == '__main__':
    TestApp().run()

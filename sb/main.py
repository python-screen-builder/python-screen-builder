import sys
import json

from kivy.app import App
from kivy.graphics import *
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.splitter import Splitter
from kivy.uix.scrollview import ScrollView

from gui import Label, Menu, SubMenu, MenuButton, MessageBox, ConfirmBox
from screen_builder import ScreenBuilder
from tkinter import filedialog as fd

from properties_layout import Property, PropertiesLayout
from settings import *

Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
sys.path.append(".") # fix path for exe version imports

class Main(App):

    version = "6.0"

    keyboard = Window.request_keyboard(None, None, 'text')
    focus = True

    def get_settings(self):
        try:
            with open("settings.json", "r") as file:
                data = file.read()
                dict = json.loads(data)
        except:
            data = default_settings
            dict = json.loads(data)

        system_settings = Settings(dict)
        return system_settings

    def build(self):
        self.settings = self.get_settings()
        self.title = 'Screen Builder'

        main_layout = BoxLayout(orientation = "vertical")
        menu = Menu(pos_hint = { 'top': 1 })
        file_menu = SubMenu(text = 'File', values = [ 'Import', 'Export', 'Exit' ])
        edit_menu = SubMenu(text = 'Edit', values = [ 'Undo', 'Copy', 'Paste', 'Delete' ])
        help_menu = SubMenu(text = 'Help', values = [ 'About' ])
        menu.add_item(file_menu)
        menu.add_item(edit_menu)
        menu.add_item(MenuButton(text = "Grid", on_press = self.show_grid))
        menu.add_item(MenuButton(text = "Clear", on_press = self.clear_screen))
        menu.add_item(help_menu)
        file_menu.handler = self.on_file
        edit_menu.handler = self.on_edit
        help_menu.handler = self.on_help
        main_layout.add_widget(menu)

        panel_layout = BoxLayout(orientation = "horizontal")
        self.screen_builder = ScreenBuilder(settings = self.settings)
        self.widgets_layout = BoxLayout(orientation = "vertical")
        self.properties_layout = PropertiesLayout()
        self.properties_layout.bind(minimum_height = self.properties_layout.setter('height'))

        widgets_splitter = Splitter(sizable_from = "right", size_hint = (.3, 1), strip_size = self.settings.strip_size)
        props_splitter = Splitter(sizable_from = "left", size_hint = (.7, 1), strip_size = self.settings.strip_size)
        
        self.build_widgets_panel()

        self.props_view = ScrollView(do_scroll_y = True, scroll_wheel_distance = 100)
        self.props_view.add_widget(self.properties_layout)

        widgets_splitter.add_widget(self.widgets_layout)
        props_splitter.add_widget(self.props_view)

        panel_layout.add_widget(widgets_splitter)
        panel_layout.add_widget(self.screen_builder)
        panel_layout.add_widget(props_splitter)

        # change to allow menu to stay on top 
        panel_layout.padding = (0, 100, 0, -100)
        main_layout.add_widget(panel_layout, 1)

        Window.size = (self.settings.window_width, self.settings.window_height)
        Window.clearcolor = self.settings.background_color
        Window.bind(on_request_close = self.on_request_close)

        self.ctrl = False
        self.shift = False
        self.keyboard.bind(on_key_down = self.on_key_down)
        self.keyboard.bind(on_key_up = self.on_key_up)

        self.main_layout = main_layout

        if len(sys.argv) > 1: self.load_file(sys.argv[1])

        return main_layout

    def on_request_close(self, *largs, **kwargs):
        if self.screen_builder.undo_count == 0: return False
        confirm = ConfirmBox(title = 'Exit the App', message = 'Are you sure?', on_confirm = self.on_confirm)
        confirm.open()
        return True
    
    def on_confirm(self):
        Clock.schedule_once(self.exit, .3)

    def exit(self, *args):
        self.stop()

    def build_widgets_panel(self):
        for widget in self.settings.widgets:
            button = Button(text = widget['name'], font_size = self.settings.font_size, on_press = self.add_screen_widget)
            button.init = widget['init']
            button.name = widget['name'].lower()
            button.file = ''
            if 'file' in widget:
                class_name = widget['class']
                button.file = widget['file']
                self.screen_builder.external_classes[class_name] = button.file
            self.widgets_layout.add_widget(button)

    def build_props_panel(self, class_name):
        self.properties_layout.widget_type.font_size = self.settings.font_size
        self.properties_layout.widget_type.text = "{0} {1}".format(class_name, "Properties")
        for property in self.properties_layout.props:
            self.properties_layout.remove_widget(property.label)
            self.properties_layout.remove_widget(property.input)
        self.properties_layout.props = []
        for widget in self.settings.widgets:
            if widget['class'] == class_name:
                for prop in widget['properties']:
                    property = Property(name = prop['name'], init = prop['init'])
                    self.properties_layout.add_property(property)
                return

    def init_properties(self, selected_widget, button = 'left'):
        self.properties_layout.set_properties(selected_widget)
        if button == 'left' and self.shift == False: self.screen_builder.bring_widget_to_top(selected_widget)
        if button == 'right': self.screen_builder.send_widget_to_back(selected_widget)

    def add_screen_widget(self, button):
        self.screen_builder.add_widget_by_name(button.text, button.init, button.name, button.file)
        self.build_props_panel(button.text)
        self.screen_builder.undo_count += 1

    def remove_screen_widget(self):
        selected_widget = self.screen_builder.get_selected_widget()
        if selected_widget == None: return
        self.screen_builder.widgets.remove(selected_widget)            
        widget = selected_widget.widget
        self.screen_builder.remove_widget(widget)
        self.screen_builder.remove_widget(selected_widget)
        if self.screen_builder.undo_count  == 0: return
        self.screen_builder.undo_count -= 1

    def get_widget_type(self, widget):
        name = type(widget).__name__
        return name

    def build_widgets_screen(self, json_widgets):
        # first clear all current screen widgets
        for dict in json_widgets:
            #print(dict)
            self.screen_builder.add_widget_from_dict(dict)

    def import_screen(self, button = None):
        if self.screen_builder.undo_count > 0: self.ask_save_changes(); return
        filename = fd.askopenfilename(initialdir = '.', filetypes = [( 'json files', '*.json' )])
        if filename == '': return
        self.screen_builder.clear_widgets()
        self.load_file(filename)

    def load_file(self, filename):
        json_widgets = []
        with open(filename, 'r') as file:
            data = file.read()
        json_widgets = json.loads(data)
        self.build_widgets_screen(json_widgets)

    def ask_save_changes(self):
        confirm = ConfirmBox(title = 'Save Changes', message = 'Save current screen?', on_confirm = self.save_changes, on_deny = self.ignore_changes)
        confirm.open()
        self.screen_builder.undo_count = 0

    def save_changes(self):
        self.export_screen()
        from kivy.clock import Clock
        Clock.schedule_once(self.import_screen, .1)

    def ignore_changes(self):
        from kivy.clock import Clock
        Clock.schedule_once(self.import_screen, .1)

    def prop_names(self, widget_type):
        prop_names = []
        for widget in self.settings.widgets:
            if widget['class'] == widget_type:
                for prop in widget['properties']:
                    if 'save' in prop and prop['save'] == False: continue
                    prop_names.append(prop['name'])
                return prop_names

    def export_screen(self, button = None):
        filename = fd.asksaveasfilename(initialdir = '.', filetypes = [( 'json files', '*.json' )], defaultextension = 'json')
        if filename == '': return
        json_widgets = []
        for select_widget in self.screen_builder.widgets:
            widget = select_widget.widget
            type = self.get_widget_type(widget)
            dict = {}
            dict['name'] = select_widget.name
            dict['type'] = type
            if type in self.screen_builder.external_classes:
                dict['file'] = self.screen_builder.external_classes[type]
            dict['x'] = widget.pos[0]
            dict['y'] = Window.height - widget.pos[1] - widget.size[1] - self.settings.menu_height
            dict['size'] = widget.size
            for prop in self.prop_names(dict['type']):
                if prop == 'name': continue
                if dict['type'] == 'Slider' and prop == 'text':
                    dict[prop] = widget.name_label.text
                    continue
                if dict['type'] == 'Knob' and prop == 'text':
                    dict[prop] = widget.label.text
                    continue
                if hasattr(widget, prop):
                    value = getattr(widget, prop)
                    if prop == 'image' and widget.image != None: value = widget.image.source
                    dict[prop] = str(value)
            json_widgets.append(dict)
        with open(filename, 'w') as file:
            file.write(json.dumps(json_widgets, ensure_ascii = False, indent = 4))
        self.screen_builder.undo_count = 0

    def show_grid(self, button):
        self.screen_builder.toggle_grid()

    def clear_screen(self, button):
        # are you sure (yes or no)?
        self.screen_builder.remove_widgets()

    def on_file(self, button):
        if button.text == 'Import': self.import_screen(button)
        if button.text == 'Export': self.export_screen(button)
        if button.text == 'Exit': self.on_exit(button)

    def on_exit(self, button):
        if self.on_request_close(button) == False: self.stop()

    def on_edit(self, button):
        if button.text == 'Undo': self.screen_builder.undo()
        if button.text == 'Copy': self.screen_builder.copy()
        if button.text == 'Paste': self.screen_builder.paste()
        if button.text == 'Delete': self.remove_screen_widget()

    def on_help(self, button):
        title = "About"
        if button.text != 'About': return
        message = Label(text = "Screen Builder " + self.version, size_hint = (1, 1))
        mb = MessageBox(title = title, message = message, size = (400, 400))
        mb.open()

    def on_key_down(self, keyboard, keycode, text, modifiers):
        # print(keycode[1])
        if self.focus == False: return
        if keycode[1] == 'a' and self.ctrl == True:
            self.screen_builder.select_all()
        if keycode[1] == 'c' and self.ctrl == True:
            self.screen_builder.copy()
        if keycode[1] == 'v' and self.ctrl == True:
            self.screen_builder.paste()
        if keycode[1] == 'z' and self.ctrl == True:
            self.screen_builder.undo()
        if keycode[1] == 'delete':
            self.remove_screen_widget()
        if keycode[1] in ('lctrl', 'rctrl'):
            self.ctrl = True
        if keycode[1] in ('shift', 'rshift'):
            self.shift = True

    def on_key_up(self, keyboard, keycode):
        # print(keycode[1])
        if self.focus == False: return
        if keycode[1] in ('lctrl', 'rctrl'):
            self.ctrl = False
        if keycode[1] in ('shift', 'rshift'):
            self.shift = False

Main().run()

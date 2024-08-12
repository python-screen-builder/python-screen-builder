from kivy.app import App
from kivy.atlas import Atlas
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from gui import Screen, Menu, SubMenu, MenuButton, Popup, Label, ListBox, Button, CheckButton
from os.path import exists

class Property():

    font_size = 25

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.init = kwargs['init']
        self.settings = App.get_running_app().settings
        self.label = Label(text = self.name, font_size = self.font_size, size_hint = (1, None), size = (0, 30))
        self.input = eval(self.init)
        self.input.size_hint = (1, None)
        try:
            self.input.bind(text = self.on_change) # , focus = self.on_focus)
        except:
            pass
        # try and set focus for text input so keys like delete will not delete the widget
        # this way the keystrokes will be directed to the text input only
        try:
            self.input.bind(focus = self.on_focus)
        except:
            pass

    def on_focus(self, instance, value):
        if value == True: App.get_running_app().focus = False
        if value == False: App.get_running_app().focus = True

    def on_change(self, instance, value):
        layout = instance.parent
        layout.on_prop_changed(self.name, value)

class PropertiesLayout(StackLayout):
    
    def __init__(self, **kwargs):
        #self.cols = 2
        super(PropertiesLayout, self).__init__(**kwargs)
        self.selected_widget = None
        self.size_hint_y = None
        self.padding = 10
        self.spacing = 20
        self.props = []
        self.widget_type = Label(size_hint = (1, None), size = (0, 30))
        self.add_widget(self.widget_type)
        pass

    def add_property(self, prop):
        # if prop type is text
        super(PropertiesLayout, self).add_widget(prop.label)
        super(PropertiesLayout, self).add_widget(prop.input)
        self.props.append(prop)
        pass

    def use_parens(self, value):
        if type(value).__name__ in ['ObservableList', 'list', 'tuple']:
            value = list(value)
            for index, number in enumerate(value):
                #number = round(number, 1)
                if type(number).__name__ == 'float': number = round(number, 1)
                value[index] = number
            
        return str(value).replace('[', '(').replace(']', ')')

    def set_widget_text(self, widget, text):
        if "Knob" in str(type(widget)):
            widget.label.text = text
        elif "Slider" in str(type(widget)):
            widget.name_label.text = text
        else:
            widget.text = text
        return 

    def get_radius(self, widget):
        if hasattr(widget, "radius"): return str(getattr(widget, "radius")[0])
        return ''

    def get_prop(self, widget, name): # return text version of prop
        if hasattr(widget, name):
            if name == 'font_size': return str(int(getattr(widget, name)))
            if name == 'image':
                if widget.image != None: return widget.image.source
                return ''
            if name == 'background_normal': return widget.background_normal
            return self.use_parens(getattr(widget, name))
        return ''

    def set_widget_image(self, widget, name):
        if widget.image != None: widget.remove_widget(widget.image)
        image = Image(source = name, allow_stretch = True)
        widget.image = image
        widget.add_widget(image)
        widget.update_handler(); widget.update_handler()

    def set_prop(self, widget, name, value):
        if hasattr(widget, name):
            #setattr(widget, name, value)
            if name == "orientation": widget.set_orientation(value); return
            if name == "image":
                # if name is valid image file
                if exists(value): self.set_widget_image(widget, value)
                if value == '':
                    if widget.image != None: widget.remove_widget(widget.image)
                    widget.image = None
                return
            if name == "background_normal":
                if value == '': widget.background_normal = ''; return
                if exists(value): widget.background_normal = value; return
                try:
                    setattr(widget, name, eval(value))
                except:
                    pass
                return
            if name == "background_down":
                if value == '': widget.background_down = ''; return
                if exists(value): widget.background_down = value; return
                try:
                    setattr(widget, name, eval(value))
                except:
                    pass
                return
            if name == "button_normal_color":
                #if value == '': widget.background_down = ''; return
                try:
                    if eval(value) == widget.button_normal_color: return
                    setattr(widget, name, eval(value))
                    widget.draw_color = widget.button_normal_color
                    widget.update_handler()
                except:
                    pass
                return
            if name == "button_down_color":
                #if value == '': widget.background_down = ''; return
                try:
                    if eval(value) == widget.button_down_color: return
                    setattr(widget, name, eval(value))
                    #widget.draw_color = widget.button_down_color
                    widget.update_handler()
                except:
                    pass
                return
            attr_value = getattr(widget, name)
            type_name = type(attr_value).__name__
            if type_name in [ 'ObservableReferenceList', 'ObservableList', 'tuple', 'list', 'int' ]:
                try:
                    setattr(widget, name, eval(value)) # ; return
                    widget.update_handler(); return # setattr(widget, name, eval(value)); return
                except:
                    return
            if type_name in [ 'str' ]:
                setattr(widget, name, value); return
            try:
                setattr(widget, name, eval(type_name + '(' + value + ')'))
            except:
                pass
            #widget.update_handler()

    def get_int(self, text):
        try:
            return int(text)
        except:
            return 0 

    def set_font(self, widget, value):
        widget.font_name = value

    def get_widget_text(self, widget):
        if "Piano" in str(type(widget)): return ''
        if "Knob" in str(type(widget)):
            return widget.label.text
        elif "Slider" in str(type(widget)):
            return widget.name_label.text
        else:
            if not hasattr(widget, 'text'): return ''
            return widget.text

    def set_properties(self, selected_widget):
        self.selected_widget = selected_widget
        widget = selected_widget.widget
        for prop in self.props:
            if prop.name == "name": prop.input.text = self.selected_widget.name; continue
            if prop.name == "text": prop.input.text = self.get_widget_text(widget); continue
            prop.input.text = self.get_prop(widget, prop.name); continue

    def on_prop_changed(self, name, value):
        if self.selected_widget == None: return
        widget = self.selected_widget.widget
        if name == "name": self.selected_widget.name = value; return
        if name == "text": self.set_widget_text(widget, value); return
        self.set_prop(widget, name, value)
        return

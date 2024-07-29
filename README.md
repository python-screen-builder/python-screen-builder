## Hi there 👋 Pythonistas and GUI enthusiasts.
The Python screen builder is an easy-to-use tool you can use to create a GUI for your python application.
The screen builder makes using Python and the Kivy framework fun and easy to use.

<img src="screenshot.png">

## Welcome to version 4.0 of the Python Screen Builder project.

### Please read if you are using version 1.0
```
The latest version of the WidgetScreen class is now subclassed directly from the Kivy Screen class.
There is also a new WidgetContainer class that works like the previous WidgetScreen class.
So, if you have a version 1.0 application, just change the WidgetScreen references to use WidgetContainer.
Please see the example test application below.
```
<marquee scrolldelay=20 loop=1>
# it is fun to program in python if you have a nice gui builder
</marquee>

## Requirements

Python, of course. The screen builder is written completely in the latest version of Python using the Kivy framework.
You will need to install Kivy in order to run the screen builder and write Python programs that use the screens.
You can find out more about how to install Kivy here:
<a href="https://kivy.org/doc/stable/gettingstarted/installation.html">Installing Kivy</a>

## Running the screen builder application
Download all of the Python files from the sb (screen builder) folder to a separate location.
Then, simply type:

```
python main.py
```
The screen builder main window should appear. You can then start building screens for your applicaiton.
The sb_test folder contains a test application (test_app.py) which you can use as a template.
There are also some other test applications that show how to program widgets and menus.

You can also compile the screen bulder to an executable if you use a python compiler, for instance: <a href="https://pyinstaller.org">pyinstaller</a>:
```
pyinstaller -F main.py
cd dist
```
You should see a file called main.exe which can be renamed for instance to something like sb.exe.

Then, you can copy it to the python scripts directory.
On Windows that might be something like: "/Program files/Python/Scripts".
```
rename main.exe sb.exe
copy sb.exe "/Program files/Python/Scripts"
```
Once the sb.exe is accessible via the system path, you can run the screen builder tool from anywhere.

Note in version 3.0, a version of the settings.json file is included in the program itself.
So, you only need to copy the settings.json file if you want modify settings.

## How to use
When you run the screen builder you can select from an array of widgets on the left sidebar.
Click Button for example to create a new button widget which will then appear on the screen.
In the properties window on the right you can change the properties of the widget.
Change its text, font, name, etc. Then File -> Export -> your_screen.json to save the screen as a JSON file.
The JSON screen file contains all the information about the controls on the screen.
Make sure the name field is filled in, which is how you can access the variable that corresponds to the screen widget.
It should automagically generate a default name, button1 for buttons, etc.

Here is the sample code for a working application that uses the screen file test_button.json
```
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
        return self.test_screen

if __name__ == '__main__':
    TestApp().run()

```
Notice the line ```self.load_screen()```. This will load the screen that you have created for your application.

If everything is working, when you run the test program:
```
python test_app.py
```
You should see a screen like this:

<img src="screenshot2.png">

Then, when you click on the button it should say something in the console window.

That's it, simple and easy to use. 😉

Here is what the code that handles a button might look like:
```
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

if __name__ == '__main__':
    TestApp().run()

```

# Documentation

## Screen Builder Keyboard and Mouse Functions
Left click a widget to bring it to the foreground.

Right click a widget to see what's behind the current one.

Note if a widget is covering another widget, you may also need to hold down ``Ctrl`` and then left click it to bring it to the foreground.

Hold down ``Ctrl`` to select multiple and then move them by using the mouse and keeping ``Ctrl`` pressed.

Hold down ``Shift`` and then left click to select a widget from behind another widget.

Press ``Del`` to delete the currently selected widget.

``Ctrl + A`` to select all screen widgets. Keep ``Ctrl`` pressed to move all objects around in the screen builder window.

``Ctrl + C`` to copy a selected widget.

``Ctrl + V`` to paste a copied widget into the screen builder window.

``Ctrl + Z`` to undo adding of the current widget.

You must currently hold down the ``Ctrl`` key when selecting widgets when using the ``Edit`` menu.

## Building an application

The screen builder contains two classes you can use to access screens from:

``WidgetScreen`` and ``WidgetContainer``

Both can be used to create the application screen.

Here is a sample application using the WidgetContainer class:

```
from gui import *
from kivy.app import App
from widget_container import WidgetContainer

class TestWidgets(WidgetContainer):

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
```
Notice that it contains a screen element that needs to point to the Kivy Screen class instance.

Both classes contain a load_screen() function that simply builds the screen from the json screen file_name parameter.

There is also a menu_height parameter you can set to the height of the application menu.

For example: ```test_screen = TestScreen(file_name = 'test_button.json', screen = screen, menu_height = 100)```

This sets the menu height to 100 pixels so that the screen widgets will not appear on top of the menu itself.

## Widget API (included in file gui.py)
To include all of the widgets to be used in the application simply use:
```
from gui import *
```
The widgets that come with the screen builder are configured to be used programatically and accept all regular Kivy parameters.
When creating a widget programmatically, you can now use x and y to position it relative to the screen upper left corner:
This enhancement gives the ability to write a more traditionally-oriented application similar to existing frameworks.
```
b = Button(x = 100, y = 100, text = "Button")
```

### Button Class
```
class Button(x = value, y = value, radius = (r1, r2, r3, r4), button_normal_color = (r, g, b, a), button_down_color = (r, g, b, a), . . .)
```
x = horizontal screen position 

y = vertical screen position

button_normal_color = color tuple to set the normal (unpressed) color of the button

button_down_color = color tuple to set the down (pressed) color of the button

radius = tuple for the roundness of the four corners of the button

border_width = thickness of the button border

border_color = color of the border

### ToggleButton Class
```
class ToggleButton(x = value, y = value, radius = (r1, r2, r3, r4), button_normal_color = (r, g, b, a), button_down_color = (r, g, b, a), . . .)
```

Example callback function using ToggleButton:

```
button = ToggleButton(x = 100, y = 100, on_press = handle_toggle)

def handle_toggle(self, instance):
    if instance.state == 'down': pass # do something if button state is down
    if instance.state == 'normal: pass # do something if button state is up
```    

### Label Class
```
class Label(x = value, y = value, text = string)
```

### Panel Class
```
class Panel(x = value, y = value, . . .)
```

### ListBox Class
```
class ListBox(x = value, y = value, . . .)
```

To initialize a list box:
```
list_box = ListBox(x = 100, y = 100, text = "apple") # set the initial item to be apple
list_box.values = [ "apple", "peaches", "pumpkin", "pie" ]
```

To add a callback to the ListBox widget:

```
list_box.bind(value = self.on_select)
.
.
def on_select(self, instance, value):
    print(value) # will print text of item selected
```

### Slider Class
```
class Slider(x = value, y = value, . . .)
```
To set the initial slider value:
```
slider.value = 100
```

To add a callback to a slider widget:

```
slider.bind(value = self.on_slider)
.
.
def on_slider(self, instance, value):
    print(value) # will print slider control value
```

### Knob Class
```
class Knob(x = value, y = value, . . .)
```
To set the initial knob value:
```
knob.value = 100
```

To add a callback to a knob widget:

```
knob.bind(value = self.on_knob)
.
.
def on_knob(self, instance, value):
    print(value) # will print knob control value
```

### Text Input Class
```
class TextInput(x = value, y = value, . . .)
```
To set the initial value:
```
text_input.text = 'hello there'
```

To add a callback to a text input widget:

```
text_input.bind(text = self.on_change)
.
.
def on_change(self, instance, value):
    print(value) # will print the current text value
```

### Switch Class
```
class Switch(x = value, y = value, . . .)
```
To set the initial value:
```
switch.active = True
```

To add a callback to a switch widget:

```
switch.bind(active = self.on_switch)
.
.
def on_switch(self, instance, value):
    print(value) # will print the current switch state
```

## Configuration
The settings.json file can be used to add or remove widgets from the sidebar pallet as well as configure other settings.

WARNING: You must be careful however when editing the settings.json file. Make a backup copy first.

Hints: to run the screen builder on Linux distros make sure to set: 

```
windows_dpi_awarensess: null
```
This will allow the Linux version to not make any Windows graphics initialization calls.

## Change Log - what is fixed in version 2.0:
- button image text can now be set back to empty string
- sometimes could not delete widget after changing some properties
- added try-except for bad int values and int to type_name list
- added set_init_pos function to reset initial position of widgets
- made radius (0, 0, 0, 0), not None for all widgets that use this property

## Enhancements to verion 2.0
- added a WidgetContainer class to replace the WidgetScreen class
- added a WidgetScreen class that subclasses directly from the Kivy Screen class
- added a button_normal_color and button_down_color for Button and Toggle widgets
- added rounded buttons to screen builder
- added start option to piano keyboard
- added save option to settings.json widget properties

## Change Log - what is fixed in version 3.0:
- fixed file open to first ask to save current screen 
- new screens loaded will clear the current screen

## Enhancements to version 3.0
- test_menu.py - example app with menu that has multiple screens
- test_widgets.py - example app that tests various widgets
- added on_deny to gui ConfirmBox
- added undo for new widgets
- added default_settings so screen builder can run without settings.json file
- added ability to use external class files in settings.json

## Version 4.0 Changes
- fixed path to allow exe version to look in current directory
- fixed list box options size to be same as list box size
- fixed radius input check for button and toggle button
- fixed layout padding for screen builder window
- added switch and text input widgets to pallet 

<!--
**python-screen-builder/python-screen-builder** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->

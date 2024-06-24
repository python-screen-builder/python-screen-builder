## Hi there 👋 pythonistas and GUI enthusiasts.

## Welcome to version 2.0 of the Python GUI Screen Builder project.

## New version 2.0 update - Please read this if you are using version 1.0

The version 2.0 of the WidgetScreen class is now subclassed directly from the Kivy Screen class.
Please see the example test application below.

There is also a new WidgetContainer class that works like the previous WidgetScreen class.
So, if you have a version 1.0 application, just change the WidgetScreen references to use WidgetContainer.

## Running the screen builder application

The Python screen builder is an easy to use tool you can use to create and load a screen for an application.
The GUI it uses is Kivy and the screen builder makes it easy and fun to use.
This is what the main screen looks like:

<img src="screenshot.png">

```
# it is fun to program in python if you have a nice gui builder
```

## Requirements

First of all, you will need to install the Kivy framework in order to run the screen builder.

You can find out how to install Kivy here:
<a href="https://kivy.org/doc/stable/gettingstarted/installation.html">Installing Kivy</a>

The latest version of the Kivy framework is what the screen builder currently uses.

## How to use

You can download all of the Python files from the sb folder to a separate location. Then, simply type:

```
python main.py
```
The screen builder main window should appear. You can then start building screens to be used with the GUI.
The sb_test folder contains the test application which you can be used as a template.

When you run the screen builder you can select from an array of GUI widgets on the sidebar.
Select a Button control for instance, change its text, font, etc. Then File -> Export -> your_screen.json to save.
The json file contains all the information about the button control you selected. Also make sure the name field is filled in.
It should automagically default to button1 for buttons. That is how you reference controls in your Python application.

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
If everything is working, when you run the test program:
```
python test_app.py
```
You should see a screen like this:

<img src="screenshot2.png">

And then when you click on the button it should say something in the console window.

That's it, simple and easy to use. 😉

## Change Log - what is fixed, new in version 2.0:

- Button image text can now be set back to empty string
- Sometimes could not delete widget after changing some properties
- added try-except for bad int values and int to type_name list
- added start=midi_key_number option to piano keyboard widget
- added set_init_pos function to reset initial position of widgets
- made radius (0, 0, 0, 0), not None for all widgets that use this property

## Enhancements in 2.0
- added a WidgetContainer class to replace the WidgetScreen class
- added a WidgetScreen class that subclasses directly from the Kivy Screen class
- added a button_normal_color and button_down_color for Button and Toggle widgets that use radius or border_width
- this allows the screen to contain both standard Kivy button functionality and rounded buttons with colors

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

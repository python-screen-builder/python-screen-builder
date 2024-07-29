class Settings:
    
    def __init__(self, dict):
        
        for key in dict:
            setattr(self, key, dict[key])

default_settings = \
"""
{
    "window_width": 1000,
    "window_height": 600,
    "windows_dpi_awareness": 2,
    "background_color": "grey",
    "default_folder": ".",
    "show_grid": false,
    "font_size": 25,
    "strip_size": 20,
    "snap_size": 20,
    "menu": [],
    "menu_height": 100,
    "fonts": [
        "Arial",
        "Roboto"
    ],
    "font_sizes": [
        "20",
        "30",
        "40",
        "50",
        "60"
    ],
    "widgets": [
        {
            "name": "Panel",
            "class": "Panel",
            "init": "Panel(background_color = (.4, .4, .4))",
            "properties": [
                {
                    "name": "name",
                    "init": "TextInput()"
                },
                {
                    "name": "text",
                    "init": "TextInput()"
                },
                {
                    "name": "halign",
                    "init": "ListBox(text = 'left', values = ['left', 'center', 'right'])"
                },
                {
                    "name": "valign",
                    "init": "ListBox(text = 'left', values = ['top', 'middle', 'bottom'])"
                },
                {
                    "name": "font_size",
                    "init": "ListBox(values = [str(x) for x in range(30, 90, 10)])"
                },
                {
                    "name": "font_name",
                    "init": "ListBox(values = self.settings.fonts)"
                },
                {
                    "name": "background_color",
                    "init": "TextInput()"
                },
                {
                    "name": "size",
                    "init": "TextInput()"
                },
                {
                    "name": "radius",
                    "init": "TextInput()"
                },
                {
                    "name": "border_width",
                    "init": "TextInput()"
                },
                {
                    "name": "border_color",
                    "init": "TextInput()"
                }
            ]
        },
        {
            "name": "Label",
            "class": "Label",
            "init": "Label()",
            "properties": [
                {
                    "name": "name",
                    "init": "TextInput()"
                },
                {
                    "name": "text",
                    "init": "TextInput()"
                },
                {
                    "name": "halign",
                    "init": "ListBox(text = 'left', values = ['left', 'center', 'right'])"
                },
                {
                    "name": "valign",
                    "init": "ListBox(text = 'left', values = ['top', 'middle', 'bottom'])"
                },
                {
                    "name": "font_size",
                    "init": "ListBox(values = [str(x) for x in range(30, 140, 10)])"
                },
                {
                    "name": "font_name",
                    "init": "ListBox(values = self.settings.fonts)"
                },
                {
                    "name": "color",
                    "init": "TextInput()"
                },
                {
                    "name": "size",
                    "init": "TextInput()"
                }
            ]
        },
        {
            "name": "Button",
            "class": "Button",
            "init": "Button()",
            "index": 1,
            "properties": [
                {
                    "name": "name",
                    "init": "TextInput()"
                },
                {
                    "name": "text",
                    "init": "TextInput()"
                },
                {
                    "name": "font_size",
                    "init": "ListBox(values = self.settings.font_sizes)"
                },
                {
                    "name": "font_name",
                    "init": "ListBox(values = self.settings.fonts)"
                },
                {
                    "name": "color",
                    "init": "TextInput()"
                },
                {
                    "name": "background_color",
                    "init": "TextInput()"
                },
                {
                    "name": "size",
                    "init": "TextInput()"
                },
                {
                    "name": "image",
                    "init": "TextInput()"
                },
                {
                    "name": "background_normal",
                    "init": "TextInput()"
                },
                {
                    "name": "radius",
                    "init": "TextInput()"
                },
                {
                    "name": "button_normal_color",
                    "init": "TextInput()"
                },
                {
                    "name": "button_down_color",
                    "init": "TextInput()"
                },
                {
                    "name": "border_width",
                    "init": "TextInput()"
                },
                {
                    "name": "border_color",
                    "init": "TextInput()"
                }
            ]
        },
        {
            "name": "Toggle",
            "class": "ToggleButton",
            "init": "ToggleButton()",
            "properties": [
                {
                    "name": "name",
                    "init": "TextInput()"
                },
                {
                    "name": "text",
                    "init": "TextInput()"
                },
                {
                    "name": "font_size",
                    "init": "ListBox(values = self.settings.font_sizes)"
                },
                {
                    "name": "font_name",
                    "init": "ListBox(values = self.settings.fonts)"
                },
                {
                    "name": "color",
                    "init": "TextInput()"
                },
                {
                    "name": "background_color",
                    "init": "TextInput()"
                },
                {
                    "name": "size",
                    "init": "TextInput()"
                },
                {
                    "name": "radius",
                    "init": "TextInput()"
                },
                {
                    "name": "button_normal_color",
                    "init": "TextInput()"
                },
                {
                    "name": "button_down_color",
                    "init": "TextInput()"
                },
                {
                    "name": "border_width",
                    "init": "TextInput()"
                },
                {
                    "name": "border_color",
                    "init": "TextInput()"
                }
            ]
        },
        {
            "name": "Program",
            "class": "ProgramButton",
            "init": "ProgramButton()",
            "properties": [
                {
                    "name": "name",
                    "init": "TextInput()"
                },
                {
                    "name": "text",
                    "init": "TextInput()"
                },
                {
                    "name": "font_size",
                    "init": "ListBox(values = self.settings.font_sizes)"
                },
                {
                    "name": "font_name",
                    "init": "ListBox(values = self.settings.fonts)"
                },
                {
                    "name": "color",
                    "init": "TextInput()"
                },
                {
                    "name": "size",
                    "init": "TextInput()"
                }
            ]
        },
        {
            "name": "List",
            "class": "ListBox",
            "init": "ListBox()",
            "properties": [
                {
                    "name": "name",
                    "init": "TextInput()"
                },
                {
                    "name": "text",
                    "init": "TextInput()"
                },
                {
                    "name": "font_size",
                    "init": "ListBox(values = self.settings.font_sizes)"
                },
                {
                    "name": "font_name",
                    "init": "ListBox(values = self.settings.fonts)"
                },
                {
                    "name": "size",
                    "init": "TextInput()"
                }
            ]
        },
        {
            "name": "Slider",
            "class": "Slider",
            "init": "Slider(orientation = 'vertical')",
            "index": 1,
            "properties": [
                {
                    "name": "name",
                    "init": "TextInput()"
                },
                {
                    "name": "text",
                    "init": "TextInput()"
                },
                {
                    "name": "orientation",
                    "init": "ListBox(text = 'vertical', values = ['horizontal', 'vertical'])"
                },
                {
                    "name": "size",
                    "init": "TextInput()"
                }
            ]
        },
        {
            "name": "Knob",
            "class": "Knob",
            "init": "Knob(size = (200, 200))",
            "properties": [
                {
                    "name": "name",
                    "init": "TextInput()"
                },
                {
                    "name": "text",
                    "init": "TextInput()"
                },
                {
                    "name": "size",
                    "init": "TextInput()"
                }
            ]
        },
        {
            "name": "Text",
            "class": "TextInput",
            "init": "TextInput()",
            "properties": [
                {
                    "name": "name",
                    "init": "TextInput()"
                }
            ]
        },
        {
            "name": "Switch",
            "class": "Switch",
            "init": "Switch()",
            "properties": [
                {
                    "name": "name",
                    "init": "TextInput()"
                }
            ]
        }
    ]
}
"""

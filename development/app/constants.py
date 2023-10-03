import json

with open("info.json", "r") as f:
    INFO = json.load(f)

with open("settings.json", "r") as f:
    SETTINGS = json.load(f)

DESCRIPTION = """
AI4C API helps you detect objects and colors in images. 🚀

## Object

...

## Color

...
"""

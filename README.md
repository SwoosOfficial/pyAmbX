# pyAMBX

A controller for philips amBX devices/kits (combustD rewritten in python)

## Requirements:

- Python3.8 or greater
- python modules: matplotlib, pyusb

### Optional for GUI:

- PyQt6

## Usage:

- CLI: use the set_color('color') directly 
with 'color' being a color recognisable by matplotlib
- GUI: adjust the sliders in RGB or HSV mode accordingly

### Examples:

- set_color('bisque')
- set_color('crimson')
- set_color('tab:blue')
- set_color((0.75,0.5,0,0)
- or reading out colormaps, yada, yada...


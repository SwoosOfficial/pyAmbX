#!./pyambx/bin/python
import usb.core as usbc

ambx_device = dict(
    usb_endpoint = 2,
    usb_init_c = '\xa1', # needs to be before all requests
    lights = dict(
        center = '\x3b',
        center_left = '\x2b',
        center_right = '\x4b',
        left = '\x0b',
        right = '\x1b',
    )
    set_light_c = '\x03',
    idVendor = 0x0471, # philips ambx
    idProduct = 0x083f, # philips ambx gaming kit
)

dev = usbc.find(
    idVendor=ambx_device['idVendor'],
    idProduct=ambx_device['idProduct'],
)

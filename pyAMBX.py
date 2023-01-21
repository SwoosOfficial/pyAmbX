#!./pyambx/bin/python
import usb.core as usbc
import matplotlib.colors as mcolor

ambx_device = dict(
    usb_endpoint = 2,
    usb_init_c = b'\xa1', # needs to be before all requests
    lights = dict(
        center = b'\x3b',
        center_left = b'\x2b',
        center_right = b'\x4b',
        left = b'\x0b',
        right = b'\x1b',
    ),
    set_light_c = b'\x03',
    idVendor = 0x0471, # philips ambx
    idProduct = 0x083f, # philips ambx gaming kit
)

def set_color(color, pos=None, ambx_device=ambx_device):
    '''
    Sets the color of the ambx device.

    Sets the color based on matplotlib colors on
    all (default) or specified positions

    Parameters:
    color (mcolor): color to set
    pos (None or tuple): tuple descriptors to set the lights
    ambx_device (dict): ambx_device as with the parameters 

    Returns:
    str: hex string sent to device
    '''

    dev = get_dev(ambx_device=ambx_device)

    if pos is None:
        pos = ambx_device['lights'].keys()

    c_bytes = get_color_bytes(color)

    for p_desc in pos:
        p = ambx_device['lights'][p_desc]
        command = p + ambx_device['set_light_c']
        comm_str = comp_comm_str(c_bytes, 
                                 command,
                                 usb_init_c=ambx_device['usb_init_c']
                                 )
        b = write_to_dev(dev, comm_str, endpoint=ambx_device['usb_endpoint'])
    dev.reset()
    return comm_str


def get_dev(ambx_device=ambx_device):
    '''gets the device'''
    dev = usbc.find(
        idVendor = ambx_device['idVendor'],
        idProduct = ambx_device['idProduct'],
    )
    if dev is None:
        raise RuntimeError('ambx device not found')
    return dev

def get_color_bytes(color):
    '''formats the matplotlib color to \\xRR\\xGG\\xBB'''
    color_tup = mcolor.to_rgba(color)
    color_ints = [int(color*255) for color in color_tup][:-1]
    return bytes(color_ints)

def comp_comm_str(arg_str, command, usb_init_c=ambx_device['usb_init_c']):
    return usb_init_c+command+arg_str

def write_to_dev(dev, string, endpoint=ambx_device['usb_endpoint']):
    '''writes a string to the usb device'''
    return dev.write(endpoint, string)

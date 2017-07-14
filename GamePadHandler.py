"""
This module handles any GamePad via HID.
"""

import pywinusb.hid as hid


class GamePadHandler(object):

    """
    Description: Handler to handle GamePad data

    Parameters:
        vendorID: Hexadecimal value for device's vendor
        productID: Hexadecimal value for device's ID
    """

    def __init__(self, vendor_id, product_id):
        """Initialize GamePadHandler"""
        self.vendor_id = vendor_id
        assert isinstance(vendor_id, int), "Not a valid VendorID, must be a hexadecimal value"
        self.product_id = product_id
        assert isinstance(product_id, int), "Not a valid ProductID, must be a hexadecimal value"
        self.leftJoyStickY = 0
        self.rightJoyStickY = 0
        self.connected = False
        self.devices = None
        self.device = None

    def sample_handler(self, data):
        """"Handle data by storing joystick Y-axis values"""
        self.leftJoyStickY = data[2]
        self.rightJoyStickY = data[4]

    def connect_to_device(self):
        """Connect to GamePad"""
        self.devices = hid.HidDeviceFilter(vendor_id=self.vendor_id, product_id=self.product_id).get_devices()
        assert self.devices, "No device found"
        self.device = self.devices[0]
        self.device.open()
        self.device.set_raw_data_handler(self.sample_handler)
        self.connected = True

    def disconnect_from_device(self):
        """Disconnect from GamePad"""
        self.device.close()
        self.connected = False

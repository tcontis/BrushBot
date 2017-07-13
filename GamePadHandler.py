import pywinusb.hid as hid

class GamePadHandler(object):

    """
    Description: Handler to handle GamePad data

    Parameters:
        vendorID: Hexadecimal value for device's vendor
        productID: Hexadecimal value for device's ID
    """

    def __init__(self,vendorID,productID):
        self.vendorID = vendorID
        assert isinstance(vendorID, int), "Not a valid VendorID, must be a hexadecimal value"
        self.productID = productID
        assert isinstance(productID, int), "Not a valid ProductID, must be a hexadecimal value"
        self.leftJoyStickY = 0
        self.rightJoyStickY = 0
        self.connected = False

    def sample_handler(self,data):
        "Handle data by storing joystick Y-axis values"
        self.leftJoyStickY = data[2]
        self.rightJoyStickY = data[4]

    def connectToDevice(self):
        "Connect to Gamepad"
        self.devices = hid.HidDeviceFilter(vendor_id=self.vendorID, product_id=self.productID).get_devices()
        assert len(self.devices) > 0, "No device found"
        self.device = self.devices[0]
        self.device.open()
        self.device.set_raw_data_handler(self.sample_handler)
        self.connected = True

    def disconnectFromDevice(self):
        "Disconnect from Gamepad"
        self.device.close()
        self.connected = False

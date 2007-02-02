import dbus

from __init__ import *

class USBDeviceInfo:
    def __init__(self, device_obj):
        self.device_obj = device_obj

        # get the device properties
        self.properties = device_obj.GetAllProperties(dbus_interface = DEV_STR)

        # get the name of the device
        self.vendor = self.properties['usb_device.vendor']
        self.product = self.properties['usb_device.product']
        self.name = self.vendor + ' -- ' + self.product

        # get the serial, vendor_id and product_id
        self.serial = self.properties['usb_device.serial']
        self.vendor_id = self.properties['usb_device.vendor_id']
        self.product_id = self.properties['usb_device.product_id']

    def __str__(self):
        return 'Vendor: %s\nVendorID: %X\nProduct: %s\nProductID: %X\nSerial: %s' % (self.vendor, self.vendor_id, self.product, self.product_id, self.serial)


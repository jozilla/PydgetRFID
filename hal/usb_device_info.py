# PydgetRFID -- a Python front-end for the Phidgets Inc. RFID kit.
# Copyright (C) 2007  Jo Vermeulen
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

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


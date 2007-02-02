import dbus

from __init__ import *
from usb_device_info import USBDeviceInfo

class DeviceManager:
    def __init__(self):
        self.initialize_dbus_and_hal()

    def initialize_dbus_and_hal(self):
        self.bus = dbus.SystemBus()

        # get Hal manager
        self.hal_manager_obj = self.bus.get_object(HAL_STR, HAL_MGR_NS_STR)
        self.hal_manager = dbus.Interface(self.hal_manager_obj, HAL_MGR_STR)

    def find(self, info = 'PhidgetRFID'):
        devices = self.hal_manager.FindDeviceStringMatch('info.product', info)
        self.matches = []

        for device in devices:
            device_obj = self.bus.get_object(HAL_STR, device)
            self.matches.append(USBDeviceInfo(device_obj))

    def __str__(self):
        str = 'Possible matches:\n-----------------'
        i = 1

        for info in dm.matches:
            str = str + '%d. %s\n~~~\n%s\n~~~' % (i, info.product, info)
            i = i + 1

        return str

if __name__ == "__main__":
    dm = DeviceManager()
    dm.find()
    print dm

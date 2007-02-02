import dbus

from common import *
from device import Device

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
            self.matches.append(Device(device_obj))


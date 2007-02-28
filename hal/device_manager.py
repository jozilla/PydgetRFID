#! /usr/bin/env python
#
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

import gobject
import dbus
if getattr(dbus, 'version', (0,0,0)) >= (0,41,0):
    import dbus.glib # for signal handlers

import sys

from __init__ import *
from usb_device_info import USBDeviceInfo


PRODUCT_STR = 'info.product'

class DeviceManager:
    def __init__(self, info = 'PhidgetRFID'):
        self.info = info
        self.current = None
        self.matches = {}
        self.initialize_dbus_and_hal()
        self.find()

    def initialize_dbus_and_hal(self):
        self.bus = dbus.SystemBus()

        # get Hal manager
        self.hal_manager_obj = self.bus.get_object(HAL_STR, HAL_MGR_NS_STR)
        self.hal_manager = dbus.Interface(self.hal_manager_obj, HAL_MGR_STR)

        # connect to signals
        self.hal_manager.connect_to_signal('DeviceAdded', self.device_added) 
        self.hal_manager.connect_to_signal('DeviceRemoved', self.device_removed)

    def find(self):
        devices = self.hal_manager.FindDeviceStringMatch('info.product', self.info)

        for device_udi in devices:
            # get info on device
            device_obj = self.bus.get_object(HAL_STR, device_udi)
            device_info = USBDeviceInfo(device_obj)

            # set current device to the first one we encounter
            self.current = device_udi
            # add it to the possible matches
            self.matches[self.current] = device_info
            
    def device_added(self, device_udi):
        # get info on device
        device_obj = self.bus.get_object(HAL_STR, device_udi)
        properties = device_obj.GetAllProperties(dbus_interface = DEV_STR)

        if PRODUCT_STR in properties and properties[PRODUCT_STR] == self.info:
            # found a match, print it out
            device_info = USBDeviceInfo(device_obj)
            print 'PhidgetRFID reader with serial %s was added' % (device_info.serial)

            # set as current device if we don't have one yet
            if self.current == None: 
                self.current = device_udi

            # add to matches
            self.matches[device_udi] = device_info
            print 'Number of matching devices: %d' % len(self.matches)
            print 'Current device serial: %s' % self.matches[self.current].serial

    def device_removed(self, device_udi):
        if device_udi in self.matches:
            serial = self.matches[device_udi].serial
            print 'PhidgetRFID reader with serial %s was removed.' % serial 

            # delete from matches
            del self.matches[device_udi]

            if self.current == device_udi:
                # current device was removed
                if len(self.matches) > 0:
                    # pick another one
                    self.current = self.matches.keys()[0]
                else:
                    # no current device
                    self.current = None

            print 'Number of matching devices: %d' % len(self.matches)
            if self.current != None:
                print 'Current device serial: %s' % self.matches[self.current].serial

    def found_match(self):
        return self.current != None and len(self.matches) > 0

    def current_device_info(self):
        if self.found_match():
            return self.matches[self.current]
        else:
            raise NoDeviceFoundError 

    def __str__(self):
        if len(self.matches) == 0:
            return "No matching devices."
        else:
            str = 'Current matching devices:\n-------------------------\n'
            i = 1
    
            for (udi, info) in self.matches.items():
                str = str + '%d. %s\n~~~\n%s\n~~~' % (i, udi, info)
                i = i + 1
    
            return str

if __name__ == "__main__":
    try:
        dm = DeviceManager()
        print dm
        mainloop = gobject.MainLoop()
        mainloop.run()
    except KeyboardInterrupt:
        sys.exit(1)

# PydgetRFID -- a Python interface for the Phidgets Inc. RFID kit.
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

from ctypes import *

TAG_NIL_VALUE = '0800000000'

class PhidgetRFID(Structure):
    """PhidgetRFID struct."""
    _fields_ = [
            ("phidget", POINTER(c_int)), # generic Phidget device  
            ("time", c_long), # time to read the tag
            ("l_tag", c_ulonglong), # tag data
            ("onboard_led", c_byte), # bool, led on?
            ("plus_five", c_byte), # bool, +5V on?
            ("external_led", c_byte), # bool, external led on?
            ("enabled", c_byte) #bool, reading on?
            ]

# phidget_return enum
(PHIDGET_RET_SUCCESS,
 PHIDGET_RET_INVALID_PARAMETER,
 PHIDGET_RET_ALREADY_INITIALISED,
 PHIDGET_RET_NOT_INITIALISED,
 PHIDGET_RET_HID_ERROR,
 PHIDGET_RET_DEVICE_ALREADY_OPENED,
 PHIDGET_RET_DEVICE_NOT_OPENED,
 PHIDGET_RET_TIMEOUT) = range(8)

# phidget_rfid_toggle enum
(PHIDGET_RFID_PLUS_FIVE,
 PHIDGET_RFID_EXTERNAL_LED,
 PHIDGET_RFID_ONBOARD_LED,
 PHIDGET_RFID_ENABLE) = range(4)

class PhidgetsError(Exception):
    def __init__(self, errno):
        self.errno = errno
        self.messages = { 
                PHIDGET_RET_INVALID_PARAMETER: 'Invalid parameter',
                PHIDGET_RET_ALREADY_INITIALISED: 'Already initialized',
                PHIDGET_RET_NOT_INITIALISED: 'Not initialized',
                PHIDGET_RET_HID_ERROR: 'Error from libhid',
                PHIDGET_RET_DEVICE_ALREADY_OPENED: 'Device already opened',
                PHIDGET_RET_DEVICE_NOT_OPENED: 'Device not opened',
                PHIDGET_RET_TIMEOUT: 'Time-out' 
                }

    def __str__(self):
        try:
            return 'PhidgetsError: %s' % self.messages[self.errno]
        except KeyError:
            return 'Unknown PhidgetsError: code %d' % self.errno

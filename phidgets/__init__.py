from ctypes import *

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

( PHIDGET_RET_SUCCESS,
  PHIDGET_RET_INVALID_PARAMETER,
  PHIDGET_RET_ALREADY_INITIALISED,
  PHIDGET_RET_NOT_INITIALISED,
  PHIDGET_RET_HID_ERROR,
  PHIDGET_RET_DEVICE_ALREADY_OPENED,
  PHIDGET_RET_DEVICE_NOT_OPENED,
  PHIDGET_RET_TIMEOUT) = range(8)

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
        return self.messages[self.errno]

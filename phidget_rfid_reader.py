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

TAG_TIME_OUT = 6000
PHIDGET_RET_SUCCESS = 0

class PhidgetRFIDReader:
    def __init__(self):
        self.dev = None
        # load dynamic library
        self.lib = cdll.LoadLibrary('libphidgets.so')
        ret = self.lib.phidget_init()
        if ret != PHIDGET_RET_SUCCESS:
            pass
            #TODO: raise error

    def open(self, usb_dev_info):
        self.lib.phidget_new_PhidgetRFID.restype = POINTER(PhidgetRFID)
        self.dev = self.lib.phidget_new_PhidgetRFID()
        self.dev_obj = self.dev.contents
        ret = self.lib.phidget_rfid_open(self.dev, 
                                         c_int(int(usb_dev_info.serial)))
        if ret != PHIDGET_RET_SUCCESS:
            pass
            #TODO: raise error

    def enable(self):
        ret = self.lib.phidget_rfid_set_state(self.dev, True, False,
                                                        False, False)
        if ret != PHIDGET_RET_SUCCESS:
            pass
            #TODO: raise error

    def read_tag(self):
        ret = self.lib.phidget_rfid_get_tag(self.dev,
                                            c_int(TAG_TIME_OUT))
        if ret != PHIDGET_RET_SUCCESS:
            pass
            #TODO: raise error

    def tag(self):
        if self.dev != None:
            return self.dev_obj.l_tag

    def time(self):
        if self.dev != None:
            return self.dev_obj.time

    def __str__(self):
        return "Tag: %010lx, Time: %lu" % (
                                               self.dev_obj.l_tag, 
                                               self.dev_obj.time
                                             )

    def __del__(self):
        if self.dev != None:
            self.lib.phidget_rfid_close(self.dev)
            self.lib.phidget_delete_PhidgetRFID(self.dev)
            self.lib.phidget_cleanup()


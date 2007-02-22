from ctypes import *
import sys

from __init__ import *

class PhidgetRFIDReader:
    def __init__(self, timeout = 6000):
        self.timeout = timeout
        self.dev = None
        # load dynamic library
        try:
            self.lib = cdll.LoadLibrary('libphidgets.so')
            ret = self.lib.phidget_init()
            self.check_errors(ret)
        except:
            print """Could not import libphidgets. Please check if it is
                     installed."""
            sys.exit(1)

    def check_errors(self, ret):
        if ret != PHIDGET_RET_SUCCESS:
            raise PhidgetsError, ret

    def open(self, usb_dev_info):
        self.lib.phidget_new_PhidgetRFID.restype = POINTER(PhidgetRFID)
        self.dev = self.lib.phidget_new_PhidgetRFID()
        self.dev_obj = self.dev.contents
        ret = self.lib.phidget_rfid_open(self.dev, 
                                         c_int(int(usb_dev_info.serial)))
        self.check_errors(ret)

    def enable(self):
        ret = self.lib.phidget_rfid_set_state(self.dev, True, False,
                                                        False, False)
        self.check_errors(ret)

    def read_tag(self):
        ret = self.lib.phidget_rfid_get_tag(self.dev,
                                            c_int(self.timeout))
        self.check_errors(ret)

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


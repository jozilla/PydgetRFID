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
            init_func = lambda: self.lib.phidget_init()
            self.call_and_check(init_func)
        except OSError, err:
            print "Could not import libphidgets: %s" % err
            sys.exit(1)

    def call_and_check(self, func):
        ret = func()
        if ret != PHIDGET_RET_SUCCESS:
            raise PhidgetsError, ret

    def open(self, usb_dev_info):
        self.lib.phidget_new_PhidgetRFID.restype = POINTER(PhidgetRFID)
        self.dev = self.lib.phidget_new_PhidgetRFID()
        self.dev_obj = self.dev.contents

        open_func = lambda: self.lib.phidget_rfid_open(
                        self.dev, c_int(int(usb_dev_info.serial))
                    )
        self.call_and_check(open_func)

    def enable(self):
        set_state_func = lambda: self.lib.phidget_rfid_set_state(
                             self.dev, True, False, False, False
                         )
        self.call_and_check(set_state_func)

    def read_tag(self):
        get_tag_func = lambda: self.lib.phidget_rfid_get_tag(
                           self.dev, c_int(self.timeout)
                       )
        self.call_and_check(get_tag_func)

    def tag(self):
        if self.dev != None:
            return '%010lx' % self.dev_obj.l_tag
        else:
            return ''

    def time(self):
        if self.dev != None:
            return '%lu' % self.dev_obj.time
        else:
            return ''

    def __str__(self):
        return "Tag: %s, Time: %s" % (self.dev_obj.l_tag, self.dev_obj.time)

    def __del__(self):
        if self.dev != None:
            try:
                close_func = lambda: self.lib.phidget_rfid_close(self.dev)
                self.call_and_check(close_func)

                # delete has no return value, so we just call it
                self.lib.phidget_delete_PhidgetRFID(self.dev)
                
                cleanup_func = lambda: self.lib.phidget_cleanup()
                self.call_and_check(cleanup_func)
            except Exception, err:
                print "While deleting PhidgetRFIDReader -- %s" % err


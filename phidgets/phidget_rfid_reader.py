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
        return "Tag: %s, Time: %s" % (self.tag(), self.time())

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


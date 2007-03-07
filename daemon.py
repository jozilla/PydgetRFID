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

import dbus
import dbus.service
if getattr(dbus, 'version', (0,0,0)) >= (0,41,0):
    import dbus.glib # for signal handlers
import gobject

from threading import Thread
import sys

from hal.device_manager import DeviceManager
from phidgets.phidget_rfid_reader import PhidgetRFIDReader
from phidgets import TAG_NIL_VALUE

class Daemon(dbus.service.Object):
    def __init__(self, bus_name, object_path="/Daemon"):
        dbus.service.Object.__init__(self, bus_name, object_path)
        self.setup()
        self.keep_reading = False
        self.reading_thread = None

    def setup(self):
        self.dm = DeviceManager()
        dev_info = self.dm.current_device_info()
        self.dev = PhidgetRFIDReader()
        self.dev.open(dev_info)
        self.dev.enable()

    @dbus.service.method('net.jozilla.PydgetRFID.DaemonInterface')
    def start_reading(self):
        """Start a loop that keeps reading RFID tags."""
        # only start the loop if we didn't do so already
        if self.keep_reading == False:
            self.keep_reading = True
    
            # start a new thread to handle the reading
            self.reading_thread = Thread(target=self.read)
            self.reading_thread.start()

    @dbus.service.method('net.jozilla.PydgetRFID.DaemonInterface')
    def stop_reading(self):
        """Stop the reading loop if it was previously started."""
        self.keep_reading = False

        # stop the reading thread (if running)
        if self.reading_thread != None:
            self.reading_thread.join() 
            self.reading_thread = None

    def read(self):
        # we keep a history of the three previous tags
        history = [self.dev.tag()] * 3
        cnt = 0
        
        while self.keep_reading:
            # do a read
            self.dev.read_tag()

            # update the history
            history[cnt % 3] = self.dev.tag()

            # variables for easy reference
            bf_prev_tag = history[(cnt-2) % 3]
            prev_tag = history[(cnt-1) % 3]
            cur_tag = history[(cnt) % 3]

            # Sometimes correct reads are alternated with nil reads.
            # Therefore we only emit the signal when (1) two (but not
            # three) nil values are read the one after the other
            # (meaning no RFID tag is near); or (2) when two different
            # values are encountered after each other (meaning a
            # different RFID tag is read), with the exception of the
            # sequence [some_tag, nil, some_tag] (which are the
            # alternating nil reads).

            if cur_tag == TAG_NIL_VALUE:
                if prev_tag == TAG_NIL_VALUE:
                    if not bf_prev_tag == TAG_NIL_VALUE:
                        self.tag_changed_signal(cur_tag) # emit signal
            else:
                if cur_tag != prev_tag:
                    if not (prev_tag == TAG_NIL_VALUE and bf_prev_tag == cur_tag):
                        self.tag_changed_signal(cur_tag) # emit signal

            cnt = cnt + 1

    @dbus.service.signal('net.jozilla.PydgetRFID.DaemonInterface')
    def tag_changed_signal(self, tag):
        """This signal is emitted when a different tag is read, with 
        the tag parameter containing the tag's value as a string.
        
        When an RFID tag is placed in the vicinity of the reader,
        tag_changed_signal is emitted only once. When we move it out
        of the reader's range, tag_changed_signal is emitted again
        just one time with the nil value we just read."""

        pass # The signal is emitted when this method exits

    @dbus.service.method('net.jozilla.PydgetRFID.DaemonInterface')
    def get_current_tag(self):
        """Get the tag that was last read by the reader."""
        return self.dev.tag()

if __name__ == '__main__':
    try:
        # needed to support threads
        gobject.threads_init()
        dbus.glib.init_threads()
    
        # setup the DBUS service
        session_bus = dbus.SessionBus()
        name = dbus.service.BusName('net.jozilla.PydgetRFID.Daemon', bus=session_bus)
        object = Daemon(name)
    
        # run the mainloop
        mainloop = gobject.MainLoop()
        mainloop.run()
    except KeyboardInterrupt:
        object.stop_reading()
        sys.exit(1)

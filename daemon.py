#! /usr/bin/env python

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
        self.keep_reading = True

        # start a new thread to handle the reading
        self.reading_thread = Thread(target=self.read)
        self.reading_thread.start()

    @dbus.service.method('net.jozilla.PydgetRFID.DaemonInterface')
    def stop_reading(self):
        self.keep_reading = False

        # stop the reading thread (if running)
        if self.reading_thread != None:
            self.reading_thread.join() 
            self.reading_thread = None

    def read(self):
        cnt = 0
        prev_tag = self.dev.tag()
        
        while self.keep_reading:
            # do a read
            self.dev.read_tag()
            cur_tag = self.dev.tag()

            # Sometimes correct reads are alternated with nil reads.
            # Therefore we only emit the signal when (1) two nil
            # values are read the one after the other (meaning no RFID
            # tag is near); or (2) when two different values are
            # encountered after each other of which the last value is
            # non-nil (meaning a different tag is read, either after a
            # nil value or after another tag).

            # two nil values
            if prev_tag == cur_tag == TAG_NIL_VALUE:
                self.tag_changed_signal(cur_tag) # emit signal
                
            # two different values of which the last is not nil
            if prev_tag != cur_tag and cur_tag != TAG_NIL_VALUE: 
                self.tag_changed_signal(cur_tag) # emit signal
                
            prev_tag = cur_tag 

    @dbus.service.signal('net.jozilla.PydgetRFID.DaemonInterface')
    def tag_changed_signal(self, tag):
        # The signal is emitted when this method exits
        pass

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

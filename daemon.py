import dbus
import dbus.service
if getattr(dbus, 'version', (0,0,0)) >= (0,41,0):
    import dbus.glib # for signal handlers
import gobject
from threading import Thread

from hal.device_manager import DeviceManager
from phidgets.phidget_rfid_reader import PhidgetRFIDReader

class Daemon(dbus.service.Object):
    def __init__(self, bus_name, object_path="/Daemon"):
        dbus.service.Object.__init__(self, bus_name, object_path)
        self.setup()
        self.keep_reading = False

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
        # stop the reading thread
        self.keep_reading = False
        self.reading_thread.join() 

    def read(self):
        tag = self.dev.tag()
        
        while self.keep_reading:
            self.dev.read_tag()
            if tag != self.dev.tag():
                tag = self.dev.tag()
                self.tag_changed_signal(tag) # emit signal

    @dbus.service.signal('net.jozilla.PydgetRFID.DaemonInterface')
    def tag_changed_signal(self, tag):
        # The signal is emitted when this method exits
        pass

if __name__ == '__main__':
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


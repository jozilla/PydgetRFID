import pygtk
pygtk.require('2.0')
import gtk

from hal.device_manager import DeviceManager
from phidgets.phidget_rfid_reader import PhidgetRFIDReader

class RFIDReader:
    def __init__(self):
        self.init_ui()
        self.init_dm()

    def init_dm(self):
        try:
            self.dm = DeviceManager()
            self.dm.find()
            self.dev_info = self.dm.matches[self.dm.current]
            self.dev = PhidgetRFIDReader()
            self.dev.open(self.dev_info)
            self.dev.enable()
        except Exception, e:
            self.err_ent.set_text(str(e))

    def init_ui(self):
        # create a window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('PhidgetRFID Reader')

        # standard event handlers
        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)

        # set border width
        self.window.set_border_width(10)

        # button
        self.read_btn = gtk.Button('Read tag')
        self.read_btn.connect('clicked', self.read_tag, None)

        # tag label and entry
        self.tag_lbl = gtk.Label('Tag: ')
        self.tag_ent = gtk.Entry()
        self.tag_ent.set_editable(False)

        # label and entry for error messages
        self.err_lbl = gtk.Label('Errors: ')
        self.err_ent = gtk.Entry()
        self.err_ent.set_text('None')
        self.err_ent.set_editable(False)

        # layout
        self.frame = gtk.VBox()

        self.tag_info = gtk.HBox()
        self.tag_info.add(self.tag_lbl)
        self.tag_info.add(self.tag_ent)

        self.err_info = gtk.HBox()
        self.err_info.add(self.err_lbl)
        self.err_info.add(self.err_ent)

        self.frame.add(self.tag_info)
        self.frame.add(self.err_info)
        self.frame.add(self.read_btn)
        self.window.add(self.frame)

        self.tag_info.show()
        self.tag_lbl.show()
        self.tag_ent.show()

        self.read_btn.show()

        self.err_info.show()
        self.err_lbl.show()
        self.err_ent.show()

        self.frame.show()

        self.window.show()

    def read_tag(self, widget, data=None):
        try:
            # clear the errors and tag entries
            self.tag_ent.set_text('')
            self.err_ent.set_text('None')

            # read a tag from the device
            self.dev.read_tag()

            # put it in the tag entry
            tag = '%010lx' % (self.dev.tag())
            self.tag_ent.set_text(tag)
        except Exception, e:
            self.err_ent.set_text(str(e))

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

if __name__ == '__main__':
    RFIDReader().main()

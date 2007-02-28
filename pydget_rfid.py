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

import pygtk
pygtk.require('2.0')
import gtk

import gobject
import dbus
if getattr(dbus, 'version', (0,0,0)) >= (0,41,0):
    import dbus.glib # for signal handlers

import sys

from hal.device_manager import DeviceManager
from phidgets.phidget_rfid_reader import PhidgetRFIDReader
from phidgets import TAG_NIL_VALUE

class RFIDReader:
    def __init__(self):
        try:
            self.init_ui()
            self.init_daemon()
        except IntrospectError:
            # daemon was not running
            print 'running daemon!'
            sys.os('python daemon.py')
            self.init_daemon()

    def init_daemon(self):
        try:
            # set up daemon
            bus = dbus.SessionBus()
            self.daemon = bus.get_object('net.jozilla.PydgetRFID.Daemon', '/Daemon')
            self.daemon_iface = dbus.Interface(self.daemon, 'net.jozilla.PydgetRFID.DaemonInterface')

            # register handler
            self.daemon.connect_to_signal('tag_changed_signal', 
                                           self.tag_changed_signal_handler, 
                                           dbus_interface='net.jozilla.PydgetRFID.DaemonInterface')
        except Exception, e:
            self.err_ent.set_text(str(e))

    def init_ui(self):
        # create a window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('PydgetRFID')

        # standard event handlers
        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)

        # set border width
        self.window.set_border_width(10)

        # button
        self.start_stop_btn = gtk.Button('Start')
        self.start_stop_btn.connect('clicked', self.start_or_stop, None)

        # tag label and entry
        self.tag_lbl = gtk.Label('Tag: ')
        self.tag_ent = gtk.Entry()
        self.tag_ent.set_editable(False)

        # label and entry for error messages
        self.err_lbl = gtk.Label('Errors: ')
        self.err_ent = gtk.Entry()
        self.err_ent.set_text('None')
        self.err_ent.set_editable(False)

        # colors for tag entry
        self.default_color = self.tag_ent.get_style().text[0]
        self.red = gtk.gdk.Color(red=50000, green=0, blue=0, pixel=0)

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
        self.frame.add(self.start_stop_btn)
        self.window.add(self.frame)

        self.tag_info.show()
        self.tag_lbl.show()
        self.tag_ent.show()

        self.start_stop_btn.show()

        self.err_info.show()
        self.err_lbl.show()
        self.err_ent.show()

        self.frame.show()

        self.window.show()

    def start_or_stop(self, widget, data=None):
        try:
            if self.start_stop_btn.get_label() == 'Start':
                # update the widgets 
                self.start_stop_btn.set_label('Stop')
                self.err_ent.set_text('None')

                # start reading
                self.daemon.start_reading(dbus_interface = 'net.jozilla.PydgetRFID.DaemonInterface')
            else:
                # update the widgets 
                self.start_stop_btn.set_label('Start')
                self.err_ent.set_text('None')

                # stop reading
                self.daemon.stop_reading(dbus_interface = 'net.jozilla.PydgetRFID.DaemonInterface')
        except Exception, e:
            self.err_ent.set_text(str(e))

    def tag_changed_signal_handler(self, tag):
        if tag == TAG_NIL_VALUE:
            self.tag_ent.modify_text(gtk.STATE_NORMAL, self.red)
        else:
            self.tag_ent.modify_text(gtk.STATE_NORMAL, self.default_color)

        self.tag_ent.set_text(tag)

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        # always stop reading
        self.daemon.stop_reading(dbus_interface = 'net.jozilla.PydgetRFID.DaemonInterface')

        gtk.main_quit()

    def main(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            sys.exit(1)

if __name__ == '__main__':
    RFIDReader().main()

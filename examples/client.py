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

import gobject
import dbus
if getattr(dbus, 'version', (0,0,0)) >= (0,41,0):
    import dbus.glib # for signal handlers

i = 0

bus = dbus.SessionBus()
remote_object = bus.get_object('net.jozilla.PydgetRFID.Daemon', '/Daemon')
iface = dbus.Interface(remote_object, 'net.jozilla.PydgetRFID.DaemonInterface')

print 'Calling start_reading ...'
remote_object.start_reading(dbus_interface = 'net.jozilla.PydgetRFID.DaemonInterface')

def tag_changed_signal_handler(tag):
    print ("Tag changed: " + tag)
    global i

    i = i + 1
    print 'i: %d' % i
    if i == 50:
        print 'Calling stop thread'
        remote_object.stop_reading(dbus_interface = 'net.jozilla.PydgetRFID.DaemonInterface')
        print 'Thread stopped'
        print 'Starting again'
        remote_object.start_reading(dbus_interface = 'net.jozilla.PydgetRFID.DaemonInterface')
        print 'OK!'
    elif i == 100:
        print 'Calling stop thread'
        remote_object.stop_reading(dbus_interface = 'net.jozilla.PydgetRFID.DaemonInterface')
        print 'Thread stopped'


remote_object.connect_to_signal('tag_changed_signal',
        tag_changed_signal_handler,
        dbus_interface='net.jozilla.PydgetRFID.DaemonInterface')

mainloop = gobject.MainLoop()
mainloop.run()


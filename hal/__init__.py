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

HAL_STR = 'org.freedesktop.Hal'
DEV_STR = 'org.freedesktop.Hal.Device'
HAL_MGR_STR = 'org.freedesktop.Hal.Manager'

HAL_MGR_NS_STR = '/org/freedesktop/Hal/Manager'

class NoDeviceFoundError(Exception):
    def __str__(self):
        return 'No suitable PhidgetRFID device was found'

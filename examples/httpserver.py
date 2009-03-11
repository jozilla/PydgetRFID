#! /usr/bin/env python
#
# PydgetRFID -- a Python front-end for the Phidgets Inc. RFID kit.
# Copyright (C) 2007-2009  Jo Vermeulen
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

import cherrypy
import time

tag_history = []

class HomePage:
    def index(self):
        return """
        <p>
            Hi, this is the PydgetRFID homepage!
        </p>"""
    index.exposed = True

class Tags:
    def __init__(self):
        self.current = CurrentTagPage()
        self.history = TagHistoryPage()

    def index(self):
        return """<p>Nothing to see here.</p>"""
    index.exposed = True

    def add(self, id = None):
        if id:
            # TODO: look up data
            tag_history.append({'id': id, 'time': time.time(), 'data': ''})
            return """<p>Tag added.</p>"""
        else:
            return """
            <form action="" method="POST">
            What tag do you want to add?
            <label for="id">ID:</label>
            <input type="text" name="id" />
            <input type="submit" />
            </form>"""
    add.exposed = True

class CurrentTagPage:
    def index(self):
        if len(tag_history) > 0:
            return """Current tag: %s""" % (tag_history[-1:])
        else:
            return """No tags read yet."""
    index.exposed = True

class TagHistoryPage:
    def index(self):
        return 'Tag history: %s' % list(reversed(tag_history))
    index.exposed = True

cherrypy.root = HomePage()
cherrypy.root.tags = Tags()

if __name__ == '__main__':
    cherrypy.config.update()
    cherrypy.server.start()


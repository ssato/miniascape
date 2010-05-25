#
# Copyright (C) 2010 Satoru SATOH <satoru.satoh at gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#

import ConfigParser as configparser
import os

from miniascape.globals import PKG_CONFIG_PATH



class ODict(dict):
    """

    >>> o = ODict()
    >>>
    >>> o['a'] = 'aaa'
    >>> assert o.a == o['a']
    >>> assert o.a == 'aaa'
    >>>
    >>> o.a = 'bbb'
    >>> assert o.a = 'bbb'
    """

    def __getattr__(self, key):
        return self.get(key, None)

    def __setattr__(self, key, val):
        self[key] = val



class Config(ODict):
    """Object holding configuration parameters.
    """

    def init(self, config_file):
        assert os.path.exists(config_file), "Config file '%s' not exists" % config_file

        cp = configparser.SafeConfigParser()
        cp.read(config_file)

        for s in cp.sections():
            x = ODict(cp.items(s))
            self[s] = x



def init(config_file=PKG_CONFIG_PATH):
    c = Config()
    c.init(config_file)

    return c


# vim:sw=4:ts=4:et:

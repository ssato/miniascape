#
# Copyright (C) 2012 Satoru SATOH <ssato@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import miniascape.config as TT  # stands for "Test Target".
import miniascape.tests.common as C

import os.path
import unittest


class Test_10_effecful_functions(unittest.TestCase):

    def test_load_metaconfs__00_no_args__load_default_metaconf_by_dir(self):
        metaconfsrc = os.path.join(C.TOPDIR, "conf.d", "META")
        confdir = os.path.abspath(os.path.join(C.TOPDIR, "conf.d", "default"))

        d = TT.load_metaconfs(metaconfsrc)

        self.assertEquals(d["confdir"], confdir)

        # see also: conf.d/META/00_main.yml
        self.assertEquals(d["guest"]["dir"], os.path.join(confdir, "guests.d"))


# vim:sw=4:ts=4:et:

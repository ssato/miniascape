#
# Copyright (C) 2013 Red Hat, Inc.
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
import miniascape.guest as TT
import miniascape.globals as G
import miniascape.tests.common as C

import os.path
import unittest


class Test_00_pure_functions(unittest.TestCase):

    def test_60_mk_distdata_g__single_guest(self):
        res = list(TT.mk_distdata_g(["foo-0"]))
        self.assertEquals(len(res), 1)

        exp = ["pkgdata0dir = /usr/share/miniascape/build/guests/foo-0",
               "dist_pkgdata0_DATA = "
               "foo-0/ks.cfg foo-0/net_register.sh foo-0/vmbuild.sh\n"]

        self.assertEquals(res[0], '\n'.join(exp))

# vim:sw=4:ts=4:et:

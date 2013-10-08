#
# Copyright (C) 2012, 2013 Red Hat, Inc.
# Red Hat Author(s): Satoru SATOH <ssato@redhat.com>
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
import tests.templates.common as C
import unittest


class Test_00(unittest.TestCase):

    def test_00_host_network_xml(self):
        ref = C.get_expected_output("00_host_network.xml")
        s = C.render("host/network.xml", "00_host_network_xml.yml")

        self.assertEquals(s, ref, C.diff(s, ref))

    def test_00_host_storagepool_xml(self):
        ref = C.get_expected_output("00_host_storagepool.xml")
        s = C.render("host/storagepool.xml", "00_host_storagepool_xml.yml")

        self.assertEquals(s, ref, C.diff(s, ref))

# vim:sw=4:ts=4:et:

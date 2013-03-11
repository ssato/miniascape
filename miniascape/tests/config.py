#
# Copyright (C) 2012, 2013 Satoru SATOH <ssato@redhat.com>
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
import miniascape.globals as G
import miniascape.tests.common as C

import os.path
import pprint
import unittest


CONFDIR = os.path.abspath(os.path.join(C.TOPDIR, "default"))


class Test_00_pure_functions(unittest.TestCase):

    def test_10_list_group_and_guests_g(self):
        self.assertEquals(
            TT.list_guest_confs("satellite", "satellite-1", CONFDIR,
                                G.M_COMMON_CONF_SUBDIR,
                                G.M_GUESTS_CONF_SUBDIR,
                                G.M_CONF_PATTERN),
            [os.path.join(CONFDIR, "common/*.yml"),
             os.path.join(CONFDIR, "guests.d/satellite/*.yml"),
             os.path.join(CONFDIR, "guests.d/satellite/satellite-1/*.yml")]
        )

    def test_20_list_net_confs(self):
        self.assertEquals(
            TT.list_net_confs("default", CONFDIR, G.M_COMMON_CONF_SUBDIR,
                              G.M_NETS_CONF_SUBDIR, G.M_CONF_PATTERN),
            [os.path.join(CONFDIR, "common/*.yml"),
             os.path.join(CONFDIR, "networks.d/*.yml"),
             os.path.join(CONFDIR, "networks.d/default/*.yml")]
        )

    def test_30_list_host_confs(self):
        self.assertEquals(
            TT.list_host_confs(CONFDIR, G.M_COMMON_CONF_SUBDIR,
                               G.M_HOST_CONF_SUBDIR, G.M_CONF_PATTERN),
            [os.path.join(CONFDIR, "common/*.yml"),
             os.path.join(CONFDIR, "host.d/*.yml")]
        )


class Test_10_effecful_functions(unittest.TestCase):

    def test_10_list_net_names(self):
        self.assertEquals(
            TT.list_net_names(CONFDIR, G.M_NETS_CONF_SUBDIR),
            ["default", "service"]
        )

    def test_20_list_group_and_guests_g(self):
        self.assertTrue(
            ("satellite", "satellite-1") in
            TT.list_group_and_guests_g(CONFDIR, G.M_GUESTS_CONF_SUBDIR)
        )

    def test_30__find_group_of_guest(self):
        self.assertEquals(
            TT._find_group_of_guest("satellite-1", CONFDIR,
                                    G.M_GUESTS_CONF_SUBDIR), "satellite")
        self.assertEquals(
            TT._find_group_of_guest("system-should-not-exist-999",
                                    CONFDIR,
                                    G.M_GUESTS_CONF_SUBDIR), None)

    def test_40_load_guest_confs(self):
        c = TT.load_guest_confs("satellite-1", "satellite", CONFDIR,
                                G.M_COMMON_CONF_SUBDIR,
                                G.M_GUESTS_CONF_SUBDIR,
                                G.M_CONF_PATTERN)
        self.assertTrue(c is not None)

    def test_50_load_host_confs(self):
        c = TT.load_host_confs(CONFDIR, G.M_COMMON_CONF_SUBDIR,
                               G.M_HOST_CONF_SUBDIR, G.M_CONF_PATTERN)
        self.assertTrue(c is not None)

    def test_60_load_guests_confs(self):
        cs = TT.load_guests_confs(CONFDIR, G.M_COMMON_CONF_SUBDIR,
                                  G.M_GUESTS_CONF_SUBDIR, G.M_CONF_PATTERN)
        self.assertTrue(cs)
        self.assertTrue(cs[0] is not None)

    def test_70_load_nets_confs(self):
        nets = TT.load_nets_confs(CONFDIR, G.M_COMMON_CONF_SUBDIR,
                                  G.M_GUESTS_CONF_SUBDIR, G.M_NETS_CONF_SUBDIR,
                                  G.M_CONF_PATTERN)
        self.assertTrue(nets)
        self.assertTrue("default" in nets.keys())
        self.assertTrue(nets.keys())


# vim:sw=4:ts=4:et:

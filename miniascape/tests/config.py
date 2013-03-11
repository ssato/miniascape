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
import unittest


CONFDIR = os.path.abspath(os.path.join(C.TOPDIR, "default"))


def _create_ConfFiles(confdir=CONFDIR,
                      common_subdir=G.M_COMMON_CONF_SUBDIR,
                      guest_subdir=G.M_GUESTS_CONF_SUBDIR,
                      net_subdir=G.M_NETS_CONF_SUBDIR,
                      host_subdir=G.M_HOST_CONF_SUBDIR,
                      pattern=G.M_CONF_PATTERN):
    return TT.ConfFiles(confdir, common_subdir, guest_subdir,
                        net_subdir, host_subdir, pattern)


class Test_00_functions(unittest.TestCase):

    def test_10_list_net_names(self):
        cf = _create_ConfFiles()
        self.assertEquals(
            TT.list_net_names(cf.netdir), ["default", "service"]
        )

    def test_20_list_group_and_guests_g(self):
        """FIXME: Write 100% inspection test for list_group_and_guests_g
        """
        cf = _create_ConfFiles()
        self.assertTrue(("satellite", "satellite-1") in
                        TT.list_group_and_guests_g(cf.guestdir))

    def test_30__find_group_of_guest(self):
        cf = _create_ConfFiles()
        self.assertEquals(TT._find_group_of_guest("satellite-1", cf.guestdir),
                          "satellite")
        self.assertEquals(
            TT._find_group_of_guest("system-should-not-exist-999",
                                    cf.guestdir), None)


class Test_10_ConfFiles(unittest.TestCase):

    def setUp(self):
        self.cf = _create_ConfFiles()

    def test_10_list_host_confs(self):
        self.assertEquals(
            self.cf.list_host_confs(),
            [os.path.join(self.cf.commondir, G.M_CONF_PATTERN),
             os.path.join(self.cf.hostdir, G.M_CONF_PATTERN)]
        )

    def test_20_list_guest_confs(self):
        ref = [os.path.join(self.cf.commondir, G.M_CONF_PATTERN),
               os.path.join(self.cf.guestdir, "satellite", G.M_CONF_PATTERN),
               os.path.join(self.cf.guestdir, "satellite/satellite-1",
                            G.M_CONF_PATTERN)]
        self.assertEquals(
            self.cf.list_guest_confs("satellite-1", "satellite"), ref
        )
        # Guess group's name:
        self.assertEquals(self.cf.list_guest_confs("satellite-1"), ref)

    def test_20_list_net_confs(self):
        self.assertEquals(
            self.cf.list_net_confs("default"),
            [os.path.join(self.cf.commondir, G.M_CONF_PATTERN),
             os.path.join(self.cf.netdir, G.M_CONF_PATTERN),
             os.path.join(self.cf.netdir, "default", G.M_CONF_PATTERN)]
        )

    def test_30_list_net_confs(self):
        """FIXME: Write tests for ConfFiles.list_net_confs.
        """
        pass

    def test_40_load_host_confs(self):
        c = self.cf.load_host_confs()
        self.assertTrue(c is not None)

    def test_50_load_guest_confs(self):
        c = self.cf.load_guest_confs("satellite-1", "satellite")
        self.assertTrue(c is not None)

        # Guess guest's group:
        c = self.cf.load_guest_confs("satellite-1")
        self.assertTrue(c is not None)

    def test_60_load_guests_confs(self):
        cs = self.cf.load_guests_confs()
        self.assertTrue(cs)
        self.assertTrue(cs[0] is not None)

    def test_70_load_nets_confs(self):
        nets = self.cf.load_nets_confs()
        self.assertTrue(nets)
        self.assertTrue("default" in nets.keys())
        self.assertTrue(nets.keys())


# vim:sw=4:ts=4:et:

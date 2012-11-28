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
import pprint
import unittest


CONFDIR = os.path.abspath(os.path.join(C.TOPDIR, "conf.d", "default"))
METACONF_DIR = os.path.join(C.TOPDIR, "conf.d", "META")


class Test_10_effecful_functions(unittest.TestCase):

    def test_00_load_metaconfs__load_by_dir(self):
        d = TT.load_metaconfs(METACONF_DIR)

        self.assertEquals(d["confdir"], CONFDIR)

        # see also: conf.d/META/00_main.yml
        self.assertEquals(d["guest"]["dir"], os.path.join(CONFDIR, "guests.d"))

    def test_02_load_metaconfs__load_by_file(self):
        metaconfsrc = os.path.join(METACONF_DIR, "00_main.yml")

        d = TT.load_metaconfs(metaconfsrc)

        self.assertEquals(d["confdir"], CONFDIR)
        self.assertEquals(d["guest"]["dir"], os.path.join(CONFDIR, "guests.d"))

    def test_10_load_guest_confs(self):
        metaconf = TT.load_metaconfs(METACONF_DIR)

        name = "rhel-6-client-1"
        d = TT.load_guest_confs(metaconf, name)

        self.assertEquals(d["hostname"], name)

    def test_20_list_guest_names(self):
        metaconf = TT.load_metaconfs(METACONF_DIR)
        guests = TT.list_guest_names(metaconf)

        self.assertNotEquals(guests, [])

    def test_22_load_guests_confs(self):
        metaconf = TT.load_metaconfs(METACONF_DIR)
        gcs = TT.load_guests_confs(metaconf)

        self.assertNotEquals(gcs, [])

    def test_30_list_net_names(self):
        metaconf = TT.load_metaconfs(METACONF_DIR)
        nets = TT.list_net_names(metaconf)

        self.assertNotEquals(nets, [])
        self.assertEquals(nets, ["default", "service"])

    def test_32_list_nets_confs(self):
        metaconf = TT.load_metaconfs(METACONF_DIR)
        ncs = TT.list_nets_confs(metaconf)

        self.assertNotEquals(ncs, [])

    def test_34__aggregate_guest_network_interfaces(self):
        metaconf = TT.load_metaconfs(METACONF_DIR)
        niss = TT._aggregate_guest_net_interfaces_g(metaconf)

        self.assertNotEquals(niss, [])

        for _n, nis in niss:
            TT._check_dups_by_ip_or_mac(nis)

    def test_40_load_host_confs(self):
        metaconf = TT.load_metaconfs(METACONF_DIR)
        c = TT.load_host_confs(metaconf)

        self.assertTrue(isinstance(c, dict))


# vim:sw=4:ts=4:et:

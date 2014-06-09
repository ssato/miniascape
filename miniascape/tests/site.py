#
# Copyright (C) 2014 Satoru SATOH <ssato@redhat.com>
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
import miniascape.site as TT
import miniascape.tests.common as C

import anyconfig
import logging
import os.path
import unittest


PKGDIR = os.path.join(C.selfdir(), "..", "..")
CTXS = os.path.join(PKGDIR, "conf/default/src.d", "*.yml")
TMPLDIR = os.path.join(PKGDIR, "templates")


# Suppress verbose logging messages from anyconfig.
anyconfig.set_loglevel(logging.WARN)


class Test_00_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_10_gen_conf_files(self):
        conf = anyconfig.load(CTXS)
        tmpldirs = [TMPLDIR]

        TT.gen_conf_files(conf, tmpldirs, self.workdir)

        dirs = ["common", "guests.d", "host.d", "networks.d"]
        for d in dirs:
            d = os.path.join(self.workdir, "default", d)
            self.assertTrue(os.path.exists(d), "dir=" + d)

# vim:sw=4:ts=4:et:

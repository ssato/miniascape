#
# Copyright (C) 2014 Satoru SATOH <ssato@redhat.com>
# License: GPLv3+
#
import miniascape.bootstrap as TT
import miniascape.utils as U
import miniascape.tests.common as C

import os.path
import unittest


TOPDIR = os.path.join(C.selfdir(), "..", "..")


class Test_00_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()

    def tearDown(self):
        # C.cleanup_workdir(self.workdir)
        pass

    def test_10_bootstrap(self):
        site = "site-A"
        TT.bootstrap(site, self.workdir, site_template="rhui",
                     site_ctxdir=os.path.join(TOPDIR, "conf"),
                     tpaths=[os.path.join(TOPDIR, "templates")])

        sitedir = os.path.join(self.workdir, site)

        self.assertTrue(os.path.exists(sitedir))
        self.assertTrue(bool(U.sglob(os.path.join(sitedir, "*.yml"))))
        for x in ("Makefile", ):
            self.assertTrue(os.path.exists(os.path.join(self.workdir, x)))

# vim:sw=4:ts=4:et:

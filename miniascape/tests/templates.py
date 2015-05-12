#
# Copyright (C) 2013 Satoru SATOH <ssato@redhat.com>
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
import miniascape.template as TT
import miniascape.tests.common as C

import anyconfig as A
import os.path
import unittest


_CONFFILE_0 = os.path.join(C.selfdir(), "00_sample.yml")
_TMPL_0 = "00_sample.tmpl"


class Test_00_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()
        self.tpaths = [C.selfdir(), self.workdir]

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_10_render_to(self):
        ctx = A.load(_CONFFILE_0)
        tmpl = _TMPL_0
        output = os.path.join(self.workdir, "tmpl.out")

        TT.render_to(tmpl, ctx, output, self.tpaths)
        self.assertTrue(os.path.exists(output))

    def test_30_compile_conf_templates(self):
        conf = A.load(_CONFFILE_0)
        tmpldirs = self.tpaths
        templates_key = "ddd_templates"

        TT.compile_conf_templates(conf, tmpldirs, self.workdir, templates_key)

        # see miniascape/tests/00_sample.yml:ddd_templates.*.dst
        self.assertTrue(os.path.exists(os.path.join(self.workdir,
                                                    "a/b/c/00_sample.out")))
        self.assertTrue(os.path.exists(os.path.join(self.workdir,
                                                    "00_sample.tmpl")))
        self.assertFalse(os.path.exists(os.path.join(self.workdir,
                                                     "dummy_out")))

# vim:sw=4:ts=4:et:

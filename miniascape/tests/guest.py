#
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
import glob
import os.path
import unittest

import miniascape.guest as TT
import miniascape.tests.common as TC


class Test_00_pure_functions(unittest.TestCase):

    def test_60_mk_distdata_g__single_guest(self):
        res = list(TT.mk_distdata_g(["foo-0"]))
        self.assertEquals(len(res), 1)

        exp = ["pkgdata0dir = /usr/share/miniascape/build/guests/foo-0",
               "dist_pkgdata0_DATA = "
               "$(shell for f in foo-0/ks.cfg foo-0/net_register.sh "
               "foo-0/vmbuild.sh; do test -f $$f && echo $$f; done)\n"]

        self.assertEquals(res[0], '\n'.join(exp))


class Test_10_arrange_setup_data(unittest.TestCase):

    def setUp(self):
        self.workdir = TC.setup_workdir()
        self.sdir = os.path.join(self.workdir, "setup")
        self.btgz = os.path.join(self.workdir, "setup.tar.xz.base64")

    def tearDown(self):
        TC.cleanup_workdir(self.workdir)

    def __common_checks(self):
        self.assertTrue(os.path.exists(self.sdir))
        self.assertTrue(os.path.isdir(self.sdir))

        self.assertTrue(os.path.exists(self.btgz))
        self.assertTrue(os.path.isfile(self.btgz))

    def test_10_single_content_data(self):
        ctx = dict(setup_data=[dict(content="aaa", dst="a.txt")])
        TT.arrange_setup_data([], ctx, self.workdir)

        out = os.path.join(self.sdir, ctx["setup_data"][0]["dst"])
        content_ref = ctx["setup_data"][0]["content"]

        self.__common_checks()

        self.assertTrue(os.path.exists(out))
        self.assertTrue(os.path.isfile(out))
        self.assertEquals(open(out).read(), content_ref)

    def test_20_single_src_data__wo_dst(self):
        fname = os.path.basename(__file__)

        ctx = dict(setup_data=[dict(src=fname)])
        TT.arrange_setup_data([TC.selfdir()], ctx, self.workdir)

        out = os.path.join(self.sdir, fname)

        self.__common_checks()

        self.assertTrue(os.path.exists(out))
        self.assertTrue(os.path.isfile(out))

    def test_22_single_src_data__w_dst(self):
        fname = os.path.basename(__file__)

        ctx = dict(setup_data=[dict(src=fname, dst="foo.txt")])
        TT.arrange_setup_data([TC.selfdir()], ctx, self.workdir)

        out = os.path.join(self.sdir, ctx["setup_data"][0]["dst"])

        self.__common_checks()

        self.assertTrue(os.path.exists(out))
        self.assertTrue(os.path.isfile(out))

    def test_24_glob_src_data(self):
        ctx = dict(setup_data=[dict(src="*.py")])
        TT.arrange_setup_data([TC.selfdir()], ctx, self.workdir)

        outs = [os.path.basename(f) for f
                in glob.glob(os.path.join(TC.selfdir(), "*.py"))]

        self.__common_checks()

        for oname in outs:
            out = os.path.join(self.sdir, oname)
            self.assertTrue(os.path.exists(out))
            self.assertTrue(os.path.isfile(out))

# vim:sw=4:ts=4:et:

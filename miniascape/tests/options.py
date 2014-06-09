#
# Copyright (C) 2012 - 2014 Satoru SATOH <ssato@redhat.com>
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
import miniascape.options as TT
import miniascape.globals as G

import unittest


class Test_00_functions(unittest.TestCase):

    def test_00__option_parser__wo_args(self):
        p = TT.option_parser()
        self.assertTrue(isinstance(p, TT.optparse.OptionParser))
        self.assertEquals(p.defaults, TT.M_DEFAULTS)

    def test_10__tweak_tmpldir_and_options(self):
        p = TT.option_parser()
        (options, _) = p.parse_args([])

        self.assertEquals(options.tmpldir, [])

        # It seems that optpare holds option values permanently so value of
        # options.tmpldir will be same even if p and options (returned from
        # p.parse_args) are re-newed:
        # options = TT.tweak_tmpldir(options)
        # self.assertEquals(options.tmpldir, [G.M_TMPL_DIR])

        (options, _) = p.parse_args(["--tmpldir", "/tmp"])

        self.assertNotEquals(options.tmpldir, [])
        self.assertEquals(options.tmpldir, ["/tmp"])

        defaults = TT.M_DEFAULTS_POST

        options = TT.tweak_tmpldir(options)
        self.assertEquals(options.tmpldir, ["/tmp", defaults["tmpldir"]])

        options = TT.tweak_options(options)

        self.assertEquals(options.tmpldir[-1], defaults["tmpldir"])
        self.assertEquals(options.ctxs, [G.site_src_ctxs()])

# vim:sw=4:ts=4:et:

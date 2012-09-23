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
import miniascape.options as O
import miniascape.globals as G

import optparse
import unittest


class Test_functions(unittest.TestCase):

    def test_option_parser__00_wo_args(self):
        p = O.option_parser()
        self.assertTrue(isinstance(p, optparse.OptionParser))
        self.assertEquals(p.defaults, O.M_DEFAULTS)

    def test_tweak_tmpldir__10(self):
        p = O.option_parser()
        (options, args) = p.parse_args([])

        self.assertEquals(options.tmpldir, [])

        # It seems that optpare holds option values permanently so value of
        # options.tmpldir will be same even if p and options (returned from
        # p.parse_args) are re-newed:
        #options = O.tweak_tmpldir(options)
        #self.assertEquals(options.tmpldir, [G.M_TMPL_DIR])

        (options, args) = p.parse_args(["--tmpldir", "/tmp"])

        self.assertNotEquals(options.tmpldir, [])
        self.assertEquals(options.tmpldir, ["/tmp"])

        options = O.tweak_tmpldir(options)
        self.assertEquals(options.tmpldir, ["/tmp", G.M_TMPL_DIR])


# vim:sw=4:ts=4:et:

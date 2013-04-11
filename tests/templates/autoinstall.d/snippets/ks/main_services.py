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
import jinja2_cli.render as R
import os.path
import os
import unittest


# FIXME: Ugly
_TEMPLATE_NAME = "main.services"
_TEMPLATE_PATH = os.path.abspath(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "../../../../../templates/autoinstall.d/snippets/ks"
))

_ENABLED_SERVICES_0 = ["iptables", "sshd"]
_DISABLED_SERVICES_0 = ["ip6tables", "mdmonitor", "rhnsd"]

_EXPECTED_RESULTS = dict(
    no_services=u"",

    only_enabled_services=u"""\
services --enabled %s""" % ','.join(_ENABLED_SERVICES_0),

    only_disabled_services=u"""\
services --disabled %s""" % ','.join(_DISABLED_SERVICES_0),

    both_enabled_and_disabled_services=u"""\
services --enabled %s --disabled %s""" % \
    (','.join(_ENABLED_SERVICES_0), ','.join(_DISABLED_SERVICES_0)),
)


def _render(ctx, tfile=_TEMPLATE_NAME, tpaths=[_TEMPLATE_PATH, os.curdir]):
    #print "file=" + tfile
    #print "tpaths=" + tpaths[0]
    return R.render(tfile, ctx, tpaths)


class Test_00_templates(unittest.TestCase):

    def helper(self, case, ctx):
        self.assertEquals(_render(ctx), _EXPECTED_RESULTS[case])

    def test_00_no_services(self):
        self.helper("no_services", dict())

    def test_10_only_enabled_services(self):
        ctx = dict(services=dict(enabled=_ENABLED_SERVICES_0))
        self.helper("only_enabled_services", ctx)

    def test_20_only_disabled_services(self):
        ctx = dict(services=dict(disabled=_DISABLED_SERVICES_0))
        self.helper("only_disabled_services", ctx)

    def test_30_both_enabled_and_disabled_services(self):
        ctx = dict(services=dict(enabled=_ENABLED_SERVICES_0,
                                 disabled=_DISABLED_SERVICES_0))
        self.helper("both_enabled_and_disabled_services", ctx)

# vim:sw=4:ts=4:et:

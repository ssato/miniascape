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
import unittest


# FIXME: Ugly
_TEMPLATE_NAME = "main.users"
_TEMPLATE_PATH = os.path.abspath(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "../../../../../templates/autoinstall.d/snippets/ks"
))

_USER_0 = dict(name="foo") 
_USER_1 = dict(name="bar", groups=["wheel", "lock"], password="secret",
               shell="/bin/zsh") 

_EXPECTED_RESULTS = dict(
    no_users=u"",
    a_user_0=u"user --name=%(name)s\n" % _USER_0,
    a_user_1=u"user --name=%s --groups=%s --password=%s --shell=%s\n" % \
        (_USER_1["name"], ','.join(_USER_1["groups"]),
         _USER_1["password"], _USER_1["shell"]),
)
_EXPECTED_RESULTS["multi_users"] = \
    _EXPECTED_RESULTS["a_user_0"] + _EXPECTED_RESULTS["a_user_1"]


def _render(ctx, tfile=_TEMPLATE_NAME, tpaths=[_TEMPLATE_PATH, os.curdir]):
    #print "file=" + tfile
    #print "tpaths=" + tpaths[0]
    return R.render(tfile, ctx, tpaths)


class Test_00_templates(unittest.TestCase):

    def helper(self, case, ctx):
        self.assertEquals(_render(ctx), _EXPECTED_RESULTS[case])

    def test_00_no_services(self):
        self.helper("no_users", dict())

    def test_10_only_enabled_services(self):
        self.helper("a_user_0", dict(users=[_USER_0, ]))

    def test_20_only_disabled_services(self):
        self.helper("a_user_1", dict(users=[_USER_1, ]))

    def test_30_both_enabled_and_disabled_services(self):
        self.helper("multi_users", dict(users=[_USER_0, _USER_1]))

# vim:sw=4:ts=4:et:

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
_TEMPLATE_NAME = "main.partitions"
_TEMPLATE_PATH = os.path.abspath(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "../../../../../templates/autoinstall.d/snippets/ks"
))

_HEAD_F = u"""\
zerombr
clearpart %s
"""

_EXPECTED_RESULTS = dict(
    autopart_0=(_HEAD_F % "--all --initlabel" + "autopart"),
    autopart_1_w_clearpart_options=(
        _HEAD_F % "--drives=vda,vdb --all" + "autopart"
    ),
    lvm_parts_0=(
        _HEAD_F % "--all --initlabel" +
        """part /boot  --size=200 --fstype ext4
part pv.100 --size=1 --grow
volgroup vg0 pv.100
logvol swap --fstype swap --name=lv_swap --vgname=vg0 --size=1024
logvol / --fstype ext4 --name=lv_root --vgname=vg0 --size=1 --grow

"""
    ),
    parts_0=(
        _HEAD_F % "--all --initlabel" +
        """part /boot  --size=200 --fstype ext4
part swap --fstype swap --size=1024
part / --size=1 --fstype ext4 --grow
"""
    ),
    parts_1=(
        _HEAD_F % "--all --initlabel" +
        """part /boot  --size=200 --fstype ext4
part swap --fstype swap --size=1024
part / --size=1 --fstype ext4 --grow
part /var --size=100 --fstype ext4
"""
    ),
)



def _render(ctx, tfile=_TEMPLATE_NAME, tpaths=[_TEMPLATE_PATH, os.curdir]):
    return R.render(tfile, ctx, tpaths)


class Test_00_templates(unittest.TestCase):

    def helper(self, case, ctx):
        self.assertEquals(_render(ctx), _EXPECTED_RESULTS[case]) #, "result=\n'%s'" % str(_render(ctx)))

    def test_00_autopart_0(self):
        self.helper("autopart_0", dict())

    def test_10_autopart_1_w_clearpart_options(self):
        ctx = dict(partitions=dict(clearpart_options="--drives=vda,vdb --all"))
        self.helper("autopart_1_w_clearpart_options", ctx)

    def test_20_lvm_parts_0(self):
        ctx = dict(partitions=dict(lvm=dict(vg="vg0",
                                            lvs=[dict(mount='/',
                                                      name="lv_root",
                                                      grow=True), ]), ), 
                   swap=1024)
        self.helper("lvm_parts_0", ctx)

    def test_30_parts_0(self):
        ctx = dict(partitions=dict(parts=[]), swap=1024)
        self.helper("parts_0", ctx)

    def test_40_parts_1(self):
        ctx = dict(partitions=dict(parts=[dict(mount='/', grow=True),
                                          dict(mount='/var', size='100')]),
                   swap=1024)
        self.helper("parts_1", ctx)

# vim:sw=4:ts=4:et:

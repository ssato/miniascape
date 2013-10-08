#
# Copyright (C) 2013 Red Hat, Inc.
# Red Hat Author(s): Satoru SATOH <ssato@redhat.com>
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


# = $topdir/test_templates/
_CURDIR = os.path.abspath(os.path.dirname(__file__)


def render(tfile, ctx={}, curdir=_CURDIR):
    tpaths = [os.path.join(curdir, "..", "templates"), curdir]
    return R.render(tfile, ctx, tpaths)


def get_expected(filename, curdir=_CURDIR):
    return os.path.join(curdir, "expected", filename).read().strip()


# vim:sw=4:ts=4:et:

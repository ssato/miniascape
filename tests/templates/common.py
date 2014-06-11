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
from __future__ import print_function

import anyconfig
import difflib
import jinja2_cli.render as R
import os.path
import sys


# = $topdir/test_templates/
_CURDIR = os.path.abspath(os.path.dirname(__file__))


def get_expected_output(filename, curdir=_CURDIR):
    """
    >>> get_expected_output("result.hello_world.j2", "/tmp/a/b")
    '/tmp/a/b/result.hello_world.j2'
    """
    return open(os.path.join(curdir, "expected", filename)).read().strip()


def load_context_from_file(filename, curdir=_CURDIR):
    return anyconfig.load(os.path.join(curdir, "contexts.d", filename))


def render(tfile, ctxfile=None, ctx={}, curdir=_CURDIR):
    tpaths = [os.path.join(curdir, "..", "..", "templates"), curdir]

    if os.path.sep in tfile:
        subdir = os.path.dirname(tfile)
        tfile = os.path.basename(tfile)
        tpaths = [os.path.join(tpaths[0], subdir)] + tpaths

    # print("tfile=%s, tpaths=%s" % (tfile, str(tpaths)), file=sys.stderr)

    if ctxfile is not None:
        ctx = load_context_from_file(ctxfile, curdir)

    return R.render(tfile, ctx, tpaths)


def diff(s, ref):
    return "\n'" + "\n".join(difflib.unified_diff(s.splitlines(),
                                                  ref.splitlines(),
                                                  'Result', 'Expected')) + "'"

# vim:sw=4:ts=4:et:

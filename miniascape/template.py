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
import jinja2_cui.render as R

import os.path
import os


def renderto(tpaths, config, tmpl, output, ask=False):
    outdir = os.path.dirname(output)

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    c = R.render(tmpl, config, tpaths, ask)
    open(output, "w").write(c)


# vim:sw=4:ts=4:et:

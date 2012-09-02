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


def mk_tmpl_cmd(tpaths, configs, output, tmpl):
    """Construct template command from given parameters.

    :param tpaths: Template path list
    :param configs: Config files
    :param output: Output file
    :param tmpl: Template file to instantiate

    >>> mk_tmpl_cmd(["a", "b/c"], ["x/y", "z/*.cfg"], "out.dat", "t.tmpl")
    'jinja2-cui -T a -T b/c -C "x/y" -C "z/*.cfg" -o out.dat t.tmpl'
    """
    params = dict(
        prog="jinja2-cui render",
        topts=' '.join("-T " + tp for tp in tpaths),
        copts=' '.join("-C \"%s\"" % c for c in configs),
        output=output,
        tmpl=tmpl,
    )

    return "%(prog)s %(topts)s %(copts)s -o %(output)s %(tmpl)s" % params


def renderto(tpaths, config, tmpl, output):
    outdir = os.path.dirname(output)

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    import logging; logging.info("tmpl=%s, tpaths=%s" % (tmpl, tpaths))
    c = R.render(tmpl, config, tpaths)
    open(output, "w").write(c)


# vim:sw=4:ts=4:et:

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
from logging import DEBUG, INFO
from miniascape.globals import M_CONF_DIR, M_TMPL_DIR, M_WORK_TOPDIR

import miniascape.utils as MU
import jinja2_cui.render as R

import glob
import logging
import optparse
import os.path
import os
import subprocess
import sys


import miniascape.guest as G
import miniascape.vnet as N

from sys import argv


def cmd2prog(c):
    return "miniascape " + c


def gen_all(argv=argv):
    p = N.option_parser(argv)
    (options, args) = p.parse_args(argv[1:])

    N.gen_vnet_files(
        options.tmpldir, options.confdir, options.workdir, options.force
    )
    G.gen_all(options.tmpldir, options.confdir, options.workdir)


# TODO: define other commands.
cmds = [("ge", "generate", gen_all), ("gu", "guest", G.main)]


def usage():
    cs = ", ".join(c for _a, c, _f in cmds)
    cas = ", ".join(a for a, _c, _f in cmds)
    print """Usage: %s COMMAND_OR_COMMAND_ABBREV [Options] [Arg ...]

Commands: %s
Command abbreviations: %s
""" % (argv[0], cs, cas)


def main(argv=argv):
    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        usage()
    else:
        cfs = [(c, f) for abbrev, c, f in cmds if argv[1].startswith(abbrev)]
        if cfs:
            (c, f) = cfs[0]
            f([cmd2prog(c)] + argv[2:])
        else:
            usage()


if __name__ == '__main__':
    main(argv)

# vim:sw=4:ts=4:et:

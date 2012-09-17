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
import miniascape.guest as G
import miniascape.utils as U
import miniascape.vnet as N

import sys


def cmd2prog(c):
    return "miniascape " + c


def gen_all(argv):
    p = N.option_parser(argv)
    p.add_option(
        "-y", "--yes", action="store_true", default=False,
        help="Assume yes for all Questions"
    )
    (options, args) = p.parse_args(argv)

    U.init_log(options.debug)

    if not options.yes:
        yesno = raw_input(
            "Are you sure to generate files from '%s' [y/n] > " % \
                options.confdir
        )
        if not yesno.strip().lower().startswith('y'):
            print >> sys.stderr, "Cancel generation of files..."
            sys.exit()

    N.gen_vnet_files(
        options.tmpldir, options.confdir, options.workdir, options.force
    )
    G.gen_all(options.tmpldir, options.confdir, options.workdir)


def init_(argv):
    N.main(argv)


# TODO: define other commands.
cmds = [
    ("i", "init", init_),
    ("ge", "generate", gen_all),
    ("gu", "guest", G.main),
    ("n", "net", N.main),
]


def usage(prog, cmds=cmds):
    cs = ", ".join(c for _a, c, _f in cmds)
    cas = ", ".join(a for a, _c, _f in cmds)
    print """\
Usage: %s COMMAND_OR_COMMAND_ABBREV [Options] [Arg ...]

Commands: %s
Command abbreviations: %s
""" % (prog, cs, cas)


def main(argv):
    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        usage(argv[0])
    else:
        cfs = [(c, f) for abbrev, c, f in cmds if argv[1].startswith(abbrev)]
        if cfs:
            (c, f) = cfs[0]
            f([cmd2prog(c)] + argv[2:])
        else:
            usage(argv[0])


if __name__ == '__main__':
    main(argv)

# vim:sw=4:ts=4:et:

#
# Copyright (C) 2012, 2013 Satoru SATOH <ssato@redhat.com>
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
import miniascape.config as C
import miniascape.guest as G
import miniascape.options as O
import miniascape.utils as U
import miniascape.host as H

import sys


def cmd2prog(c):
    return "miniascape " + c


def gen_all(argv):
    p = H.option_parser()
    (options, args) = p.parse_args(argv)

    U.init_log(options.verbose)
    options = O.tweak_tmpldir(options)

    cf = C.ConfFiles(options.confdir)

    H.gen_host_files(cf, options.tmpldir, options.workdir, options.force)
    G.gen_all(cf, options.tmpldir, options.workdir)


# TODO: define other commands.
cmds = [
    ("i", "init", H.main),
    ("ge", "generate", gen_all),
    ("gu", "guest", G.main),
]


def usage(prog, cmds=cmds):
    cs = ", ".join(c for _a, c, _f in cmds)
    cas = ", ".join(a for a, _c, _f in cmds)
    print """\
Usage: %s COMMAND_OR_COMMAND_ABBREV [Options] [Arg ...]

Commands: %s
Command abbreviations: %s
""" % (prog, cs, cas)


def main(argv=sys.argv):
    assert not U.is_superuser(), \
           "Danger! You should NOT run this program as root!"

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
    main(sys.argv)

# vim:sw=4:ts=4:et:

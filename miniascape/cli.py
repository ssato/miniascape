#
# Copyright (C) 2012 - 2014 Satoru SATOH <ssato@redhat.com>
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
from miniascape.globals import LOGGER as logging, set_loglevel

import miniascape.bootstrap as B
import miniascape.config as C
import miniascape.guest as G
import miniascape.options as O
import miniascape.host as H
import miniascape.site as S

import os
import sys


def is_superuser():
    return os.getuid() == 0


def cmd2prog(c):
    return "miniascape " + c


def build(argv):
    """
    Configure and build files.
    """
    defaults = dict(build=True, genconf=True, **O.M_DEFAULTS)

    p = O.option_parser(defaults)
    p.add_option("--no-build", action="store_false", dest="build",
                 help="Do not build, generate ks.cfg, vm build scripts, etc.")
    p.add_option("--no-genconf", action="store_false", dest="genconf",
                 help="Do not generate config from context files")
    (options, args) = p.parse_args(argv)

    options = O.tweak_options(options)
    set_loglevel(options.verbose)

    # configure
    if options.genconf:
        confdir = S.configure(options.ctxs, options.tmpldir, options.workdir)

    if not options.build:
        return

    # ... and build (generate all).
    cf = C.ConfFiles(confdir)

    H.gen_host_files(cf, options.tmpldir, options.workdir, True)
    G.gen_all(cf, options.tmpldir, options.workdir)


# format: (<abbrev>, <command>, <function_to_call>)
CMDS = [("bo", "bootstrap", B.main,
         "Bootstrap site config files from ctx src and conf templates"),
        ("b",  "build", build,
         "build (generate) outputs from tempaltes and context files"),
        ("c",  "configure", build, "Same as the above ('build')")]


def usage(prog, cmds=CMDS):
    cs = "\n".join("\t%s (abbrev: %s)\t%s" % (c, a, h) for a, c, _f, h in cmds)
    print """Usage: %s COMMAND_OR_COMMAND_ABBREV [Options] [Arg ...]

Commands:
  %s
""" % (prog, cs)


def main(argv=sys.argv):
    assert not is_superuser(), "Danger! Do NOT run this program as root!"

    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        usage(argv[0])
    else:
        cfs = [(c, f) for abbrev, c, f, _h in cmds
               if argv[1].startswith(abbrev)]
        if cfs:
            (c, f) = cfs[0]
            f([cmd2prog(c)] + argv[2:])
        else:
            usage(argv[0])


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

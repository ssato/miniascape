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
from miniascape.globals import LOGGER as logging, set_loglevel, \
    M_GUESTS_CONF_SUBDIR

import miniascape.bootstrap as B
import miniascape.config as C
import miniascape.guest as G
import miniascape.options as O
import miniascape.utils as U
import miniascape.host as H
import miniascape.site as S

import datetime
import glob
import multiprocessing
import subprocess
import sys


def timestamp():
    return datetime.datetime.now().strftime("%F_%T")


def cmd2prog(c):
    return "miniascape " + c


def gen_all(argv):
    p = H.option_parser()
    (options, args) = p.parse_args(argv)

    options = O.tweak_tmpldir(options)
    set_loglevel(options.verbose)

    cf = C.ConfFiles(options.confdir)

    H.gen_host_files(cf, options.tmpldir, options.workdir, options.force)
    G.gen_all(cf, options.tmpldir, options.workdir)


def configure_and_build(argv):
    defaults = dict(build=True, **O.M_DEFAULTS)

    p = O.option_parser(defaults)
    p.add_option("--no-build", action="store_false", dest="build",
                 help="Build (generate ks.cfg, vm build scripts, etc.) also")
    (options, args) = p.parse_args(argv)

    options = O.tweak_options(options)
    set_loglevel(options.verbose)

    # configure
    conf = S.load_site_ctxs(options.ctxs)
    S.gen_site_conf_files(conf, options.tmpldir, options.workdir)

    if not options.build:
        return

    # ... and build (generate all).
    cf = C.ConfFiles(options.confdir)

    H.gen_host_files(cf, options.tmpldir, options.workdir, True)
    G.gen_all(cf, options.tmpldir, options.workdir)


# TODO: define other commands.
cmds = [
    # ("i", "init", H.main),
    ("bo", "bootstrap", B.main,
     "Bootstrap site config files from ctx src and conf templates"),
    ("c",  "configure", configure_and_build,
     "Generate site configuration from config src and build (generate all)"),
    ("b",  "build", configure_and_build, "Same as the above"),
    ("ge", "generate", gen_all,
     "Generate all files to build guests and virt. infra"),
    ("gu", "guest", G.main, "Generate files to build specific guest"),
]


def usage(prog, cmds=cmds):
    cs = "\n".join("\t%s (abbrev: %s)\t%s" % (c, a, h) for a, c, _f, h in cmds)
    print """Usage: %s COMMAND_OR_COMMAND_ABBREV [Options] [Arg ...]

Commands:
  %s
""" % (prog, cs)


def main(argv=sys.argv):
    assert not U.is_superuser(), \
        "Danger! You should NOT run this program as root!"

    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        usage(argv[0])
    else:
        cfs = [
            (c, f) for abbrev, c, f, _h in cmds if argv[1].startswith(abbrev)
        ]
        if cfs:
            (c, f) = cfs[0]
            f([cmd2prog(c)] + argv[2:])
        else:
            usage(argv[0])


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

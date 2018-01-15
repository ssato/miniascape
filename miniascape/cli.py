#
# Copyright (C) 2012 - 2018 Satoru SATOH <ssato@redhat.com>
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
import logging
import os
import sys

import miniascape.bootstrap
import miniascape.config
import miniascape.globals
import miniascape.guest
import miniascape.host
import miniascape.options
import miniascape.site


def is_superuser():
    return os.getuid() == 0


def cmd2prog(c):
    return "miniascape " + c


def build(argv):
    """
    Configure and build files.
    """
    defaults = dict(build=True, genconf=True, **miniascape.options.M_DEFAULTS)

    p = miniascape.options.option_parser(defaults)
    p.add_option("--no-build", action="store_false", dest="build",
                 help="Do not build, generate ks.cfg, vm build scripts, etc.")
    p.add_option("--no-genconf", action="store_false", dest="genconf",
                 help="Do not generate config from context files")
    (options, args) = p.parse_args(argv)

    miniascape.globals.set_loglevel(options.verbose)
    options = miniascape.options.tweak_options(options)

    # suppress logs from anyconfig unless the environment variable
    # 'ANYCONFIG_DEBUG' is set to 1.
    if os.environ.get("ANYCONFIG_DEBUG", None) != '1':
        logging.getLogger("anyconfig").setLevel(logging.WARN)

    # configure
    if options.genconf:
        confdir = miniascape.site.configure(options.ctxs, options.tmpldir,
                                            options.workdir, options.site)

    if not options.build:
        return

    # ... and build (generate all).
    cf = miniascape.config.ConfFiles(confdir)

    miniascape.host.gen_host_files(cf, options.tmpldir, options.workdir, True)
    miniascape.guest.gen_all(cf, options.tmpldir, options.workdir)


# format: (<alias>, <command>, <function_to_call>)
_CMDS = [("bo", "bootstrap", miniascape.bootstrap.main,
          "Bootstrap site config files from ctx src and conf templates"),
         ("b",  "build", build,
          "build (generate) outputs from tempaltes and context files"),
         ("c",  "configure", build, "Same as the above ('build')")]


_USAGE = """Usage: {} COMMAND_OR_COMMAND_ALIAS [Options] [Arg ...]

Commands:
  {}
"""


def usage(prog, cmds=_CMDS, usage=_USAGE):
    cs = ("\t{} (alias: {})\t{}".format(c, a, h) for a, c, _f, h in cmds)
    print(usage.format(prog, '\n'.join(cs)))


def main(argv=sys.argv, cmds=_CMDS):
    assert not is_superuser(), "Danger! Do NOT run this program as root!"

    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        usage(argv[0])
    else:
        cfs = [(c, f) for alias, c, f, _h in cmds
               if argv[1].startswith(alias)]
        if cfs:
            (c, f) = cfs[0]
            f([cmd2prog(c)] + argv[2:])
        else:
            usage(argv[0])


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

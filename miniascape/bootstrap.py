#
# Copyright (C) 2014 Red Hat, Inc.
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
from miniascape.globals import LOGGER as logging, set_loglevel, M_TMPL_DIR
import miniascape.options as O
import miniascape.template as T
import miniascape.utils as U

import anyconfig as AC
import os.path
import os
import sys


def mk_ctx(input_file):
    """
    :param input_file: Path to input YAML file may have empty parameters
    """
    ctx = AC.load(input_file)

    for key_path, val, d in U.walk(ctx):
        if val is None:
            val = raw_input("%s: " % key_path)
        else:
            val_new = raw_input("%s [%s]: " % (key_path, val))
            if val_new:
                val = val_new  # update it unless user gave empty value.

        d[key_path.split('.')[-1]] = val

    return ctx


def bootstrap(ctx_input_path, conf_tmpldir, workdir, tpaths):
    """
    :param ctx_input_path: Context input path, ex. ~/tmp/input/10_site.yml.in
    :param conf_tmpldir: Config templates dir, ex. ~/templates/bootstrap
    :param workdir: Working dir
    """
    ctx = mk_ctx(ctx_input_path)
    AC.dump(ctx, os.path.join(workdir, "ctx.yml"))

    for dirpath, dirnames, filenames in os.walk(conf_tmpldir):
        reldir = dirpath.replace(conf_tmpldir + os.path.sep, '')

        for fn in filenames:
            fn_base, ext = os.path.splitext(fn)

            if ext == ".j2":
                output = os.path.join(workdir, reldir, fn_base)
                T.renderto([dirpath] + tpaths, ctx, fn, output)
            else:
                output = os.path.join(workdir, reldir, fn)
                T.renderto([dirpath] + tpaths, {}, fn, output)


def option_parser():
    defaults = dict(conf_tmpldir=os.path.join(M_TMPL_DIR, "bootstrap"),
                    **O.M_DEFAULTS)
    defaults["confdir"] = None

    p = O.option_parser(defaults, "%prog [OPTION ...]")
    p.add_option("", "--conf-tmpldir", help="Config template dir [%default]")
    return p


def main(argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    set_loglevel(options.verbose)
    options = O.tweak_tmpldir(options)

    if not options.confdir:
        options.confdir = raw_input("Specify config (ctx) src dir: ")

    if not options.conf_tmpldir:
        options.conf_tmpldir = os.path.join(M_TMPL_DIR, "bootstrap")

    bootstrap(ctx_input_path, options.conf_tmpldir, workdir, options.tmpldir)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

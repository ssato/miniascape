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


def mk_ctx(input_file, ask=True):
    """
    :param input_file: Path to input YAML file may have empty parameters
    :param ask: Use default value and do not ask user if True
    """
    ctx = AC.load(input_file, "yaml")

    # Workaround for the "dictionary changed size during iteration" error.
    xs = list(U.walk(ctx))

    for key_path, val, d in xs:
        if val is None:
            val = raw_input("%s: " % key_path)
            if not val:
                raise RuntimeError("Invalid value entered: key=%s, val=%s" %
                                   (key_path, str(val)))
        elif ask:
            val_new = raw_input("%s [%s]: " % (key_path, val))
            if val_new:
                val = val_new  # update it unless user gave empty value.
        else:
            pass  # Just use the default: val

        key = key_path.split('.')[-1]
        d[key] = val

    return ctx


def bootstrap(ctx_input_path, conf_tmpldir, workdir, tpaths, ask=True):
    """
    :param ctx_input_path: Context input path, ex. ~/tmp/input/10_site.yml.in
    :param conf_tmpldir: Config templates dir, ex. ~/templates/bootstrap
    :param workdir: Working dir
    :param tpaths: Template search paths
    :param ask: Use default value and do not ask user if True
    """
    ctx = mk_ctx(ctx_input_path, ask)
    site = ctx.get("site", "site")

    if not os.path.exists(workdir):
        os.makedirs(workdir)

    AC.dump(ctx, os.path.join(workdir, "ctx.yml"))

    for dirpath, dirnames, filenames in os.walk(conf_tmpldir):
        reldir = dirpath.replace(conf_tmpldir, '').replace("site", site)
        logging.debug("conf_tmpldir=%s, reldir=%s, dirpath=%s" %
                      (conf_tmpldir, reldir, dirpath))

        for fn in filenames:
            (fn_base, ext) = os.path.splitext(fn)

            if ext == ".j2":
                logging.debug("Jinja2 template found: " + fn)
                T.renderto([dirpath] + tpaths, ctx, fn,
                           os.path.join(workdir, reldir, fn_base))
            else:
                T.renderto([dirpath] + tpaths, {}, fn,
                           os.path.join(workdir, reldir, fn))


def option_parser():
    defaults = dict(conf_tmpldir=os.path.join(M_TMPL_DIR, "confsrc"),
                    ask=True, **O.M_DEFAULTS)

    p = O.option_parser(defaults, "%prog [OPTION ...] CONF_SRC")
    p.add_option("", "--conf-tmpldir",
                 help="Config templates dir to walk [%default]")
    p.add_option("", "--no-ask", action="store_false", dest="ask",
                 help="Do not ask user and just use default value if set")
    return p


def main(argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    set_loglevel(options.verbose)
    options = O.tweak_tmpldir(options)

    if not args:
        p.print_usage()
        sys.exit(1)

    bootstrap(args[0], options.conf_tmpldir, options.workdir, options.tmpldir,
              options.ask)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

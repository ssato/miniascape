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
# from __future__ import absolute_import
from __future__ import print_function

from miniascape.globals import LOGGER as logging, set_loglevel, M_TMPL_DIR
import miniascape.globals as G
import miniascape.options as O
import miniascape.template as T
import miniascape.utils as U

import anyconfig as AC
import os.path
import os
import sys


def _ctx_files_pattern(site_pattern, ctx_topdir=G.M_CONF_TOPDIR,
                       subdir=G.M_BOOTSTRAP_SUBDIR,
                       ctx_pattern=G.M_CONF_PATTERN):
    """
    >>> _ctx_files_pattern("foo", "/etc/miniascape.d", "bootstrap", "*.yml")
    '/etc/miniascape.d/foo/bootstrap/*.yml'
    """
    return os.path.join(ctx_topdir, site_pattern, subdir, G.M_CONF_PATTERN)


def mk_ctx(input_file, use_default=False):
    """
    :param input_file: Path to input YAML file may have empty parameters
    :param use_default: Use default value and do not ask user if default was
        given and this parameter is True
    """
    ctx = AC.load(input_file, "yaml")

    # Workaround for the "dictionary changed size during iteration" error.
    xs = list(U.walk(ctx))

    for key_path, val, d in xs:
        if val is None:
            val = raw_input("{}: ".format(key_path))
            if not val:
                raise RuntimeError("Invalid value entered: key={}, "
                                   "val={}".format(key_path, str(val)))
        elif use_default:
            pass  # Just use the default: val
        else:
            val_new = raw_input("{} [{}]: ".format(key_path, val))
            if val_new:
                val = val_new  # update it unless user gave empty value.

        key = key_path.split('.')[-1]
        d[key] = val

    return ctx


def bootstrap(site_pattern, ctx_files, tpaths, workdir, use_default=False):
    """
    Bootstrap the site by generating configuration files from ctx files may
    lack of some configuration parameters and configuration templates.

    :param site_pattern: Site pattern name, ex. "default".
    :param ctx_files: Context files pattern or file path,
        ex. "~/tmp/foo/bootstrap/*.yml", "~/tmp/bar/bootstrap/00.yml".
    :param tpaths: Template search paths,
        ex. ["/usr/share/miniascape/templates", '.'].
    :param workdir: Working dir to save results.
    :param use_default: Use default value and do not ask user if default was
        given and this parameter is True.
    """
    ctx = mk_ctx(ctx_files, use_default)
    site = ctx.get("site", "site")

    if not os.path.exists(workdir):
        os.makedirs(workdir)

    AC.dump(ctx, os.path.join(workdir, "ctx.yml"))

    for tmpldir in tpaths:
        conf_tmpldir = os.path.join(tmpldir, "config", site_pattern)

        if not os.path.exists(conf_tmpldir):
            continue

        if not conf_tmpldir.endswith(os.path.sep):
            conf_tmpldir += os.path.sep

        logging.debug("conf_tmpldir: " + conf_tmpldir)

        for dirpath, dirnames, filenames in os.walk(conf_tmpldir):
            reldir = dirpath.replace(conf_tmpldir, '').replace("site", site)
            logging.debug("conf_tmpldir={}, reldir={}, "
                          "dirpath={}".format(conf_tmpldir, reldir, dirpath))

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
    defaults = dict(site_pattern='default', ctx=None, use_default=False,
                    list_site_patterns=False, confdir=G.site_confdir(),
                    **O.M_DEFAULTS)

    p = O.option_parser(defaults, "%prog [OPTION ...]")
    p.add_option("-S", "--site-pattern",
                 help="Specify the site pattern [%default]")
    p.add_option("-L", "--list-site-patterns", action="store_true",
                 help="List available site patterns other than 'default'")
    p.add_option("-C", "--ctx",
                 help="Specify the context files pattern or ctx file path")
    p.add_option("-U", "--use-default", action="store_true",
                 help="Just use default value if set w/o asking users")
    p.add_option("-c", "--confdir",
                 help="Top dir to hold site configuration files or "
                      "configuration file [%default]")
    return p


def main(argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    set_loglevel(options.verbose)
    options = O.tweak_options(options)

    if options.list_site_patterns:
        sps = [os.path.basename(sp) for sp in
               U.sglob(os.path.join(options.tmpldir[0], "config", '*'))
               if os.path.isdir(sp)]
        print("Site patterns other than 'default': " + ", ".join(sps))
        sys.exit(0)

    if not options.ctx:
        options.ctx = _ctx_files_pattern(options.site_pattern,
                                         options.confdir.replace("default",
                                                                 ''))

    bootstrap(options.site_pattern, options.ctx, options.tmpldir,
              options.workdir, options.use_default)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

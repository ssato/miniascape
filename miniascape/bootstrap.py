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


def bootstrap(site, workdir, site_template=G.M_SITE_DEFAULT,
              site_ctxdir=G.M_CONF_TOPDIR, tpaths=[]):
    """
    Bootstrap the site by arranging default configuration files.

    :param site: Site name, ex. "default".
    :param workdir: Working dir to save results.
    :param site_template: Site template name, ex. "default".
    :param site_ctxdir: Top dir to hold sites' template configuration files
    :param tpaths: Templates path list
    """
    ctx = dict(site=site, workdir=workdir, site_template=site_template)
    ctx_outdir = os.path.join(workdir, site)

    if not os.path.exists(ctx_outdir):
        logging.info("Creating site ctx dir: " + ctx_outdir)
        os.makedirs(ctx_outdir)

    for conf in U.sglob(os.path.join(site_ctxdir, site_template, "*.yml")):
        os.symlink(os.path.abspath(conf),
                   os.path.join(ctx_outdir, os.path.basename(conf)))

    for tmpldir in (os.path.join(d, "bootstrap", site_template) for d
                    in tpaths):
        if not tmpldir.endswith(os.path.sep):
            tmpldir += os.path.sep

        for dirpath, dirnames, filenames in os.walk(tmpldir):
            reldir = dirpath.replace(tmpldir, '')
            logging.debug("tmpldir={}, reldir={}, "
                          "dirpath={}".format(tmpldir, reldir, dirpath))

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
    defaults = dict(site_template=G.M_SITE_DEFAULT, **O.M_DEFAULTS)

    p = O.option_parser(defaults, "%prog [OPTION ...]")
    p.add_option("", "--site-template",
                 help="Site template name, e.g. default, rhui. [%default]")
    return p


def main(argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    set_loglevel(options.verbose)
    options = O.tweak_options(options)

    bootstrap(options.site, options.workdir, options.site_template,
              tpaths=options.tmpldir)

if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

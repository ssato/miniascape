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
from miniascape.globals import LOGGER as logging

import miniascape.globals as G
import optparse


M_DEFAULTS = dict(tmpldir=[], ctxs=[], site=None, workdir=G.M_WORK_TOPDIR,
                  verbose=1)

M_DEFAULTS_POST = dict(tmpldir=G.M_TMPL_DIR, site=G.M_SITE_DEFAULT)


def option_parser(defaults=M_DEFAULTS, usage="%prog [OPTION ...]"):
    """
    :param defaults: Default option values :: dict
    :param usage: Usage text
    """
    p = optparse.OptionParser(usage)
    p.set_defaults(**defaults)

    ctxs_0 = G.site_src_ctx().replace(G.M_SITE_DEFAULT, "<site>")

    p.add_option("-t", "--tmpldir", action="append",
                 help="Template top dir[s] [[%s]]" % G.M_TMPL_DIR)
    p.add_option("-s", "--site", help="Choose site [%default]")
    p.add_option("-C", "--ctx", dest="ctxs", action="append",
                 help="Specify context (conf) file[s] or path glob "
                      "pattern or dir (*.yml will be searched). It can be "
                      "given multiple times to specify multiple ones, ex. "
                      "-C /a/b/c.yml -C '/a/d/*.yml' -C /a/e/ "
                      "[%s]. This option is only supported in some sub "
                      "commands, configure and bootstrap." % ctxs_0)
    p.add_option("-w", "--workdir",
                 help="Working dir to output results [%default]")
    p.add_option("-v", "--verbose", action="store_const", const=0,
                 dest="verbose", help="Verbose mode")
    p.add_option("-q", "--quiet", action="store_const", const=2,
                 dest="verbose", help="Quiet mode")
    return p


def _default_ctxs(site):
    dctxs = G.site_src_ctx(site)
    logging.info("Site default ctxs: site={}, default={}".format(site, dctxs))
    return dctxs


def tweak_options(options, defaults_post=M_DEFAULTS_POST):
    """
    This function will be called after options and args parsed, and tweak
    options as needed such like:

    - ensure system template path is always included or appended at the tail of
      template search list
    - ensure default context file is always included at least or at the top of
      contexts list

    :param options: An instance of optparse.Values holding option values
    """
    default_tmpldir = defaults_post["tmpldir"]

    # Default template path is always included in the list of template paths as
    # the lowest priority path.
    if default_tmpldir not in options.tmpldir:
        options.tmpldir.append(default_tmpldir)

    if options.ctxs:
        if options.site:
            # Insert the default ctxs path at the head of ctxs list (the lowest
            # priority) only if options.site is set.
            options.ctxs.insert(0, _default_ctxs(options.site))

        # NOTE: Maybe it's better to untouch it and to be set from ctx.
        # else:
        #    options.site = defaults_post["site"]
    else:
        if options.site is None:
            options.site = defaults_post["site"]

        options.ctxs = [_default_ctxs(options.site)]

    return options

# vim:sw=4:ts=4:et:

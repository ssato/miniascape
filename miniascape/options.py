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
import miniascape.globals as G
import optparse


M_DEFAULTS = dict(tmpldir=[], confdir=G.M_CONFDIR_DEFAULT, ctxs=[],
                  workdir=G.M_WORK_TOPDIR, verbose=1)

M_DEFAULTS_POST = dict(tmpldir=G.M_TMPL_DIR, ctxs=G.M_CTXS_DEFAULT)


def option_parser(defaults=M_DEFAULTS, usage="%prog [OPTION ...]"):
    """
    :param defaults: Default option values :: dict
    :param usage: Usage text
    """
    p = optparse.OptionParser(usage)
    p.set_defaults(**defaults)

    p.add_option("-t", "--tmpldir", action="append",
                 help="Template top dir[s] [[%s]]" % G.M_TMPL_DIR)
    p.add_option("-c", "--confdir",
                 help="Top dir to hold site configuration files or "
                      "configuration file [%default]")
    p.add_option("-C", "--c", dest="ctxs", action="append",
                 help="Specify context (conf) file[s] or path glob "
                      "pattern or dir (*.yml will be searched). It can be "
                      "given multiple times to specify multiple ones, ex. "
                      "-C /a/b/c.yml -C '/a/d/*.yml' -C /a/e/ "
                      "[%s]" % G.M_CTXS_DEFAULT)
    p.add_option("-w", "--workdir",
                 help="Working dir to output results [%default]")
    p.add_option("-v", "--verbose", action="store_const", const=0,
                 dest="verbose", help="Verbose mode")
    p.add_option("-q", "--quiet", action="store_const", const=2,
                 dest="verbose", help="Quiet mode")
    return p


def tweak_tmpldir(options):
    """
    This function will be called after options and args parsed, and ensure
    system template path is always appended to the tail of search list.
    """
    if G.M_TMPL_DIR not in options.tmpldir:
        options.tmpldir.append(G.M_TMPL_DIR)

    return options


def tweak_options(options, defaults=M_DEFAULTS_POST):
    """
    This function will be called after options and args parsed, and tweak
    options as needed such like:

    - ensure system template path is always included or appended at the tail of
      template search list
    - ensure default context file is always included at least or at the top of
      contexts list
    """
    if G.M_TMPL_DIR not in options.tmpldir:
        options.tmpldir.append(defaults["tmpldir"])

    if options.ctxs:
        # NOTE: We have to give lowest priority to the default ctxs.
        options.ctxs.insert(0, defaults[ctxs])
    else:
        options.ctxs = [defaults["ctxs"]]

    return options

# vim:sw=4:ts=4:et:

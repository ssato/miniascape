#
# Copyright (C) 2012 Satoru SATOH <ssato@redhat.com>
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


M_DEFAULTS = dict(tmpldir=[], confdir=G.M_CONFDIR_DEFAULT,
                  workdir=G.M_WORK_TOPDIR, verbose=1)


def option_parser(defaults=M_DEFAULTS, usage="%prog [OPTION ...]"):
    p = optparse.OptionParser(usage)
    p.set_defaults(**defaults)

    p.add_option("-t", "--tmpldir", action="append",
                 help="Template top dir[s] [[%s]]" % G.M_TMPL_DIR)
    p.add_option("-c", "--confdir",
                 help="Top dir to hold site configuration files [%default]")
    p.add_option("-w", "--workdir",
                 help="Working dir to output results [%default]")
    p.add_option("-D", "--debug", action="store_const", const=0,
                 dest="verbose", help="Debug mode")
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


# vim:sw=4:ts=4:et:

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
from glob import glob
from logging import DEBUG, INFO

import miniascape.template as T
import miniascape.utils as U
import miniascape.vnet as V

import logging
import optparse
import os.path
import os
import sys
import yaml


def gen_files(tmpldir, confdir, workdir):
    outdir = os.path.join(workdir, "host")
    conf = yaml.load(confdir, "host.yml")

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    xss = [
        (p, os.path.basename(p) for p in
            glob(os.path.join(tmpldir, "host/*") if os.path.isfile(p)
    ]

    for t, n in xss:
        o = os.path.join(outdir, n)
        logging.debug("Generating host file: " + o)
        T.renderto([os.path.join(tmpldir, "host")], conf, t, o)



def option_parser(argv=sys.argv, defaults=None):
    if defaults is None:
        defaults = dict(
            tmpldir=M_TMPL_DIR,
            confdir=M_CONF_DIR,
            workdir=M_WORK_TOPDIR,
            debug=False,
        )

    p = optparse.OptionParser("%prog [OPTION ...]", prog=argv[0])
    p.set_defaults(**defaults)

    p.add_option("-t", "--tmpldir", help="Template top dir [%default]")
    p.add_option("-c", "--confdir",
        help="Configuration files top dir [%default]"
    )
    p.add_option("-w", "--workdir", help="Working top dir [%default]")
    p.add_option("-D", "--debug", action="store_true", help="Debug mode")

    return p


def main(argv):
    p = option_parser(argv)
    (options, args) = p.parse_args(argv[1:])

    logging.getLogger().setLevel(DEBUG if options.debug else INFO)

    gen_files(options.tmpldir, options.confdir, options.workdir):


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

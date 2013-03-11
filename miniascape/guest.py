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
from miniascape.globals import M_TMPL_DIR, M_WORK_TOPDIR, M_GUESTS_CONF_SUBDIR

import miniascape.config as C
import miniascape.options as O
import miniascape.template as T
import miniascape.utils as U

import logging
import optparse
import os.path
import os
import re
import subprocess
import sys


_AUTOINST_SUBDIR = "autoinstall.d"


def _workdir(topdir, name, subdir=M_GUESTS_CONF_SUBDIR):
    """
    :param topdir: Working top dir
    :param name: Guest's name
    :return: Guest's working (output) directory
    """
    return os.path.join(topdir, subdir, name)


def arrange_setup_data(gtmpldirs, config, gworkdir):
    """
    Arrange setup data to be embedded in kickstart files.

    :param gtmpldirs: Guest's template dirs :: [path]
    :param config: Guest's config :: dict
    :param gworkdir: Guest's workdir
    """
    tmpls = config.get("setup_data", [])
    if not tmpls:
        return  # Nothing to do.

    for t in tmpls:
        src = t.get("src", None)
        assert src is not None, "Lacks 'src'"

        dst = t.get("dst", src)
        out = os.path.join(gworkdir, "setup", dst)
        tpaths = gtmpldirs + \
            [os.path.join(d, os.path.dirname(src)) for d in gtmpldirs] + \
            [os.path.dirname(out)]

        logging.info("Generating %s from %s" % (out, src))
        T.renderto(tpaths, config, src, out, ask=True)

    subprocess.check_output(
        "tar --xz -c setup | base64 > setup.tar.xz.base64",
        shell=True, cwd=gworkdir
    )


def gen_guest_files(name, conffiles, tmpldirs, workdir):
    """
    Generate files (vmbuild.sh and ks.cfg) to build VM `name`.

    :param name: Guest's name
    :param conffiles: ConfFiles object
    :param tmpldirs: Template dirs :: [path]
    :param workdir: Working top dir
    """
    conf = conffiles.load_guest_confs(name)
    gtmpldirs = [os.path.join(d, _AUTOINST_SUBDIR) for d in tmpldirs]

    if not os.path.exists(workdir):
        logging.debug("Creating working dir: " + workdir)
        os.makedirs(workdir)

    logging.info("Generating setup data archive to embedded: " + name)
    arrange_setup_data(gtmpldirs, conf, workdir)

    for k, v in conf.get("templates", {}).iteritems():
        if not v.get("src", False) or not v.get("dst", False):
            continue

        (src, dst) = (v["src"], v["dst"])
        if os.path.sep in src:
            srcdirs = [os.path.join(d, os.path.dirname(src)) for d in tmpldirs]
        else:
            srcdirs = tmpldirs

        # strip dir part as it will be searched from srcdir.
        src = os.path.basename(src)
        dst = os.path.join(workdir, dst)

        logging.info("Generating %s from %s [%s]" % (dst, src, k))
        T.renderto(srcdirs + [workdir], conf, src, dst)


def show_vm_names(conffiles):
    """
    :param conffiles: config.ConfFiles object
    """
    print >> sys.stderr, "\nAvailable VMs: " + \
        ", ".join(conffiles.list_guest_names())


def gen_all(cf, tmpldirs, workdir):
    """
    Generate files to build VM for all VMs.

    :param conffiles: config.ConfFiles object
    :param tmpldirs: Template dirs :: [path]
    :param workdir: Working top dir
    """
    for name in cf.list_guest_names():
        gen_guest_files(name, cf, tmpldirs, _workdir(workdir, name))


def option_parser():
    defaults = dict(genall=False, **O.M_DEFAULTS)
    p = O.option_parser(defaults, "%prog [OPTION ...] [GUEST_NAME]")

    p.add_option("-A", "--genall", action="store_true",
                 help="Generate configs for all guests")
    return p


def main(argv=sys.argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    U.init_log(options.verbose)
    options = O.tweak_tmpldir(options)

    cf = C.ConfFiles(options.confdir)

    if not args and not options.genall:
        p.print_help()
        show_vm_names(cf)
        sys.exit(0)

    if options.genall:
        gen_all(cf, options.tmpldir, options.workdir)
    else:
        name = args[0]
        gen_guest_files(
            name, cf, options.tmpldir, _workdir(options.workdir, name)
        )


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

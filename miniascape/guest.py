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
from miniascape.globals import M_CONF_DIR, M_TMPL_DIR, M_WORK_TOPDIR
from logging import DEBUG, INFO

import miniascape.template as T
import miniascape.utils as MU

import glob
import logging
import optparse
import os.path
import os
import subprocess
import sys


def _mk_workdir(name, topdir=M_WORK_TOPDIR):
    return os.path.join(topdir, name)


def gen_guest_files(name, tmpldir, confdir, workdir):
    """
    Generate files (vmbuild.sh and ks.cfg) to build VM `name`.
    """
    workdir = os.path.join(workdir, name)
    confs = [
        os.path.join(confdir, "common/*.yml"),  # e.g. confdir/common/00.yml
        os.path.join(confdir, "guests.d/%s.yml" % name),
    ]

    conf = MU.load_confs(confs)
    kscfg = conf.get("kscfg", "%s-ks.cfg" % name)

    kscmd = T.mk_tmpl_cmd(
        [os.path.join(tmpldir, "autoinstall.d")], confs,
        os.path.join(workdir, "ks.cfg"),
        os.path.join(tmpldir, "autoinstall.d", kscfg),
    )
    vbcmd = T.mk_tmpl_cmd(
        [os.path.join(tmpldir, "libvirt")], confs,
        os.path.join(workdir, "vmbuild.sh"),
        os.path.join(tmpldir, "libvirt", "vmbuild.sh"),
    )

    if not os.path.exists(workdir):
        logging.info("Creating working dir: " + workdir)
        os.makedirs(workdir)

    logging.debug("Generating kickstart config: " + kscmd)
    subprocess.check_output(kscmd, shell=True)

    logging.debug("Generating vm build script: " + vbcmd)
    subprocess.check_output(vbcmd, shell=True)


def _cfg_to_name(config):
    """
    >>> _cfg_to_name("/etc/miniascape/config/guests.d/abc.yml")
    'abc'
    """
    return  os.path.basename(os.path.splitext(config)[0])


def list_names(confdir):
    return sorted(
        _cfg_to_name(f) for f in
            glob.glob(os.path.join(confdir, "guests.d/*.yml"))
    )


def show_vm_names(confdir):
    print >> sys.stderr, "\nAvailable VMs: " + ", ".join(list_names(confdir))


def option_parser(defaults=None):
    if defaults is None:
        defaults = dict(
            tmpldir=M_TMPL_DIR,
            confdir=M_CONF_DIR,
            workdir=M_WORK_TOPDIR,
            debug=False,
        )

    p = optparse.OptionParser("%prog [OPTION ...] NAME")
    p.set_defaults(**defaults)

    p.add_option("-t", "--tmpldir", help="Template top dir [%default]")
    p.add_option("-c", "--confdir", help="Configurations (context files) top dir [%default]")
    p.add_option("-w", "--workdir", help="Working top dir [%default]")

    p.add_option("-D", "--debug", action="store_true", help="Debug mode")

    return p


def main(argv=sys.argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    if not args:
        p.print_help()
        show_vm_names(options.confdir)
        sys.exit(0)

    logging.getLogger().setLevel(DEBUG if options.debug else INFO)

    vmname = args[0]
    gen_guest_files(vmname, options.tmpldir, options.confdir, options.workdir)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

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


def _workdir(topdir, name):
    return os.path.join(topdir, name)


def list_guest_confs(confdir, name):
    return [
        os.path.join(confdir, "common/*.yml"),  # e.g. confdir/common/00.yml
        os.path.join(confdir, "guests.d/%s.yml" % name),
    ]


def load_guest_confs(confdir, name):
    return MU.load_confs(list_guest_confs(confdir, name))


def arrange_setup_data(gtmpldir, config, gworkdir):
    """
    Arrange setup data embedded in kickstart files.

    :param gtmpldir: Guest's template dir
    :param config: Guest's config :: dict
    :param gworkdir: Guest's workdir, e.g. workdir/foo
    """
    tmpls = config.get("setup_data", [])
    if not tmpls:
        return  # Nothing to do.

    for t in tmpls:
        src = t.get("src", None)
        assert src is not None, "Lacks 'src'"

        dst = t.get("dst", src)
        out = os.path.join(gworkdir, "setup", dst)

        logging.info("Generating %s from %s" % (out, src))
        T.renderto([gtmpldir, os.path.dirname(out)], config, src, out)

    subprocess.check_output(
        cmd = "tar --xz -c setup | base64 > setup.tar.xz.base64",
        shell=True, cwd=gworkdir
    )


def gen_guest_files(name, tmpldir, confdir, workdir):
    """
    Generate files (vmbuild.sh and ks.cfg) to build VM `name`.
    """
    conf = load_guest_confs(confdir, name)
    kscfg = conf.get("kscfg", "%s-ks.cfg" % name)
    gtmpldir = os.path.join(tmpldir, "autoinstall.d")

    if not os.path.exists(workdir):
        logging.debug("Creating working dir: " + workdir)
        os.makedirs(workdir)

    logging.info("Generating setup data archive: " + name)
    arrange_setup_data(gtmpldir, conf, workdir)

    logging.info("Generating vm build data: " + name)
    T.renderto(
        [gtmpldir, workdir], conf, kscfg, os.path.join(workdir, "ks.cfg"),
    )
    T.renderto(
        [os.path.join(tmpldir, "libvirt"), workdir],
        conf, "vmbuild.sh", os.path.join(workdir, "vmbuild.sh")
    )


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


def gen_all(tmpldir, confdir, workdir):
    for name in list_names(confdir):
        gen_guest_files(name, tmpldir, confdir, _workdir(workdir, name))


def option_parser(defaults=None):
    if defaults is None:
        defaults = dict(
            tmpldir=M_TMPL_DIR,
            confdir=M_CONF_DIR,
            workdir=None,
            genall=False,
            debug=False,
        )

    p = optparse.OptionParser("%prog [OPTION ...] [NAME]")
    p.set_defaults(**defaults)

    p.add_option("-t", "--tmpldir", help="Template top dir [%default]")
    p.add_option("-c", "--confdir",
        help="Configurations (context files) top dir [%default]"
    )
    p.add_option("-w", "--workdir",
        help="Working dir to dump results [%s/<NAME>]" % M_WORK_TOPDIR
    )
    p.add_option("-A", "--genall", action="store_true",
        help="Generate configs for all guests"
    )

    p.add_option("-D", "--debug", action="store_true", help="Debug mode")

    return p


def main(argv=sys.argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    if not args and not options.genall:
        p.print_help()
        show_vm_names(options.confdir)
        sys.exit(0)

    logging.getLogger().setLevel(DEBUG if options.debug else INFO)

    if options.genall:
        if options.workdir is None:
            options.workdir = M_WORK_TOPDIR

        gen_all(options.tmpldir, options.confdir, options.workdir)
    else:
        name = args[0]
        if options.workdir is None:
            options.workdir = os.path.join(M_WORK_TOPDIR, name)

        gen_guest_files(
            name, options.tmpldir, options.confdir, options.workdir
        )


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

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
from miniascape.globals import M_CONF_DIR, M_TMPL_DIR, M_WORK_TOPDIR, \
    M_COMMON_CONFDIR

import miniascape.template as T
import miniascape.utils as U

import glob
import logging
import optparse
import os.path
import os
import re
import subprocess
import sys


_GUEST_SUBDIR = "guests.d"
_GROUP_SUBDIR = "sysgroups.d"
_AUTOINST_SUBDIR = "autoinstall.d"


def _workdir(topdir, name):
    """
    :param topdir: Working top dir
    :param name: Guest's name
    """
    return os.path.join(topdir, _GUEST_SUBDIR, name)


def _guestconfdir(confdir, name):
    """
    :param confdir: Config topdir
    :param name: Guest's name
    """
    return os.path.join(confdir, _GUEST_SUBDIR, name)


def _sysgroup(name):
    """
    FIXME: Ugly.

    >>> _sysgroup('rhel-5-cluster-1')
    'rhel-5-cluster'
    >>> _sysgroup('cds-1')
    'cds'
    >>> _sysgroup('satellite')
    'satellite'
    """
    return name[:name.rfind('-')] if re.match(r".+-\d+$", name) else name


def _groupconfdir(confdir, name):
    """
    :param confdir: Config topdir
    :param name: Guest's name
    """
    return os.path.join(confdir, _GROUP_SUBDIR, _sysgroup(name))


def common_confs(confdir):
    """
    :param confdir: Config topdir
    """
    d = os.path.join(confdir, M_COMMON_CONFDIR)

    assert os.path.exists(d), "Could not find common confdir: " + d
    return os.path.join(d, "*.yml")


def group_confs(confdir, name):
    """
    :param confdir: Config topdir
    :param name: Guest's name
    """
    d = _groupconfdir(confdir, name)
    return os.path.join(d, "*.yml") if os.path.exists(d) else None


def guest_confs(confdir, name):
    """
    :param confdir: Config topdir
    :param name: Guest's name
    """
    d = _guestconfdir(confdir, name)

    assert os.path.exists(d), "Could not find guest's confdir: " + name
    return os.path.join(d, "*.yml")  # e.g. /.../guests.d/<name>/00.yml


def list_guest_confs(confdir, name):
    """
    :param confdir: Config topdir
    :param name: Guest's name
    """
    return [
        x for x in [common_confs(confdir),
                    group_confs(confdir, name),
                    guest_confs(confdir, name)] if x is not None
    ]


def load_guest_confs(confdir, name):
    """
    :param confdir: Config topdir
    :param name: Guest's name
    """
    logging.info("Loading %s's config from %s" % (name, confdir))

    return T.load_confs(list_guest_confs(confdir, name))


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


def gen_guest_files(name, tmpldirs, confdir, workdir):
    """
    Generate files (vmbuild.sh and ks.cfg) to build VM `name`.
    """
    conf = load_guest_confs(confdir, name)
    gtmpldirs = [os.path.join(d, _AUTOINST_SUBDIR) for d in tmpldirs]

    if not os.path.exists(workdir):
        logging.debug("Creating working dir: " + workdir)
        os.makedirs(workdir)

    logging.info("Generating setup data archive to embedded: " + name)
    arrange_setup_data(gtmpldirs, conf, workdir)

    for k, v in conf.get("templates", {}).iteritems():
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


def _cfg_to_name(config):
    """
    >>> _cfg_to_name("/etc/miniascape/config/guests.d/abc.yml")
    'abc'
    """
    return  os.path.basename(os.path.splitext(config)[0])


def list_names_g(confdir):
    for x in glob.glob(os.path.join(confdir, "guests.d/*")):
        if os.path.isfile(x) and x.endswith(".yml"):
            yield _cfg_to_name(x)
        else:
            yield os.path.basename(x)


def list_names(confdir):
    return sorted(list_names_g(confdir))


def show_vm_names(confdir):
    print >> sys.stderr, "\nAvailable VMs: " + ", ".join(list_names(confdir))


def gen_all(tmpldirs, confdir, workdir):
    for name in list_names(confdir):
        gen_guest_files(name, tmpldirs, confdir, _workdir(workdir, name))


def load_guests_confs(confdir):
    return [load_guest_confs(confdir, n, 1) for n in list_names(confdir)]


def option_parser(defaults=None):
    if defaults is None:
        defaults = dict(
            tmpldir=[], confdir=M_CONF_DIR, workdir=None, genall=False,
            debug=False,
        )

    p = optparse.OptionParser("%prog [OPTION ...] [NAME]")
    p.set_defaults(**defaults)

    p.add_option("-t", "--tmpldir", action="append",
        help="Template top dir[s] [[%s]]" % M_TMPL_DIR
    )
    p.add_option("-c", "--confdir",
        help="Configurations (context files) top dir [%default]"
    )
    p.add_option("-w", "--workdir",
        help="Working dir to dump results [%s/guests.d/<NAME>]" % M_WORK_TOPDIR
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

    U.init_log(options.debug)

    # System template path is always appended to the tail of search list.
    options.tmpldir.append(M_TMPL_DIR)

    if options.genall:
        if options.workdir is None:
            options.workdir = M_WORK_TOPDIR

        gen_all(options.tmpldir, options.confdir, options.workdir)
    else:
        name = args[0]
        if options.workdir is None:
            options.workdir = os.path.join(M_WORK_TOPDIR, name)

        gen_guest_files(
            name, options.tmpldir, options.confdir,
            _workdir(options.workdir, name)
        )


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

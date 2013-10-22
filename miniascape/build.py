#
# VM (guest) builder.
#
# Copyright (C) 2012, 2013 Satoru SATOH <ssato@redhat.com>
# Copyright (C) 2013 Red Hat, Inc.
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
from miniascape.globals import LOGGER as logging, set_loglevel, \
    M_VMBUILD_SH, M_SITE_DEFAULT, M_GUESTS_BUILDDATA_TOPDIR

import miniascape.site as S

import glob
import multiprocessing
import optparse
import os.path
import subprocess
import sys


def builders_topdir(topdir=M_GUESTS_BUILDDATA_TOPDIR, site=M_SITE_DEFAULT):
    return os.path.join(topdir, site)


def builder_path(name, topdir=M_GUESTS_BUILDDATA_TOPDIR, site=M_SITE_DEFAULT,
                 vmbuild_sh=M_VMBUILD_SH):
    """
    Make up the vm (guest) build script path.
    """
    return os.path.join(builders_topdir(topdir, site), name, vmbuild_sh)


def _get_site_and_name(path, topdir=M_GUESTS_BUILDDATA_TOPDIR):
    """
    >>> _get_site_and_name("/a/b/c/d/e/f", "/a/b/c")
    ['d', 'e']
    """
    return [x for x in path.replace(topdir, '', 1).split(os.path.sep) if x][:2]


def flip(pair):
    """
    >>> flip([1, 2])
    (2, 1)
    """
    return (pair[1], pair[0])


def find_site_by_name(name, topdir=M_GUESTS_BUILDDATA_TOPDIR):
    """
    :param name: VM name to find out
    :return: Site's name of the target VM
    """
    candidates = glob.glob(builder_path(name, topdir, '*'))

    if not candidates:
        logging.warn("Could not find VM '%s' in any sites" % name)
        return None

    if len(candidates) > 1:
        name_and_sites = [flip(_get_site_and_name(c)) for c in candidates]
        cs = '\n'.join("\t#%d: %s (site: %s)" % (i, n, s) for i, n, s in
                       enumerate(name_and_sites))
        cidx = raw_input("Which VM to choose ? Select No. from\n" + cs)
        try:
            return name_and_sites[int(cidx)][1]
        except:
            raise RuntimeError("Wrong No.: " + str(cidx))
    else:
        return _get_site_and_name(candidates[0])[-1]


def build_vm_cmd_g(name, topdir=M_GUESTS_BUILDDATA_TOPDIR, site=M_SITE_DEFAULT,
                   verbose=False, log=None):
    """
    :param name: VM's name
    :param topdir: Top dir where guests' build data exist
    :param site: Site name to find and build guests from
    :param verbose: Verbose mode
    :param log: Log file name or None (not logged)
    """
    yield "bash -x" if verbose else "bash"
    yield builder_path(name, topdir, site)  # cmd

    if log is not None:
        yield " 2>&1 | tee " + log


def build_vm_cmd(name, topdir=M_GUESTS_BUILDDATA_TOPDIR, site=M_SITE_DEFAULT,
                 verbose=False, log=None):
    """
    Make up a list of command strings to build VM (guest) of given ``name``.

    :param name: VM's name
    :param topdir: Top dir where guests' build data exist
    :param site: Site name to find and build guests from
    :param verbose: Verbose mode
    :param log: Log file name or None (not logged)
    """
    return ' '.join(build_vm_cmd_g(name, topdir, site, verbose, log))


def build_vm(name=None, topdir=M_GUESTS_BUILDDATA_TOPDIR, site=None,
             verbose=False, log=None, dryrun=False):
    """
    :param name: VM's name
    :param topdir: Top dir where guests' build data exist
    :param site: Site name to find and build guests from
    :param verbose: Verbose mode
    :param log: Log file name or None (not logged)
    :param dryrun: Just return command to run if True
    """
    if name is None:
        name = raw_input("VM name ? : ")

    if site is None:
        site = find_site_by_name(name, topdir)

    c = build_vm_cmd(name, topdir, site, verbose, log)
    logging.debug("Build VM: cmd=" + c)

    if dryrun:
        return True

    # @throw subprocess.CalledProcessError
    return subprocess.check_call(c, shell=True)


def _name_from_builder_path(path):
    """
    >>> p = "/usr/share/miniascape/build/guests/foobar/baz/vmbuild.sh"
    >>> _name_from_builder_path(p)
    'baz'
    """
    return path.split(os.path.sep)[-2]


def list_all_vm_for_site(topdir=M_GUESTS_BUILDDATA_TOPDIR,
                         site=M_SITE_DEFAULT):
    return [_name_from_builder_path(p) for p in
            glob.glob(builder_path('*', topdir, site))]


def build_vm_0(kwargs):
    return build_vm(**kwargs)


def build_vms(vms, nprocs, topdir=M_GUESTS_BUILDDATA_TOPDIR,
              site=M_SITE_DEFAULT, verbose=False, log=None,
              dryrun=False):
    """
    """
    pool = multiprocessing.Pool(nprocs)
    res = pool.map_async(build_vm_0,
                         [dict(name=n, topdir=topdir, site=site,
                               verbose=verbose, log=log,
                               dryrun=dryrun) for n in vms])
    pool.close()
    pool.join()


_USAGE = """%prog [Options] VM_NAME_0 [VM_NAME_1 ...]
  where VM_NAME_X   Name of the VM to build, or special keyword 'all' to
                    build all of VMs in the site.
"""


_NPROCS = multiprocessing.cpu_count() * 2


def option_parser(usage=_USAGE, nprocs=_NPROCS):
    defaults = dict(topdir=M_GUESTS_BUILDDATA_TOPDIR, site=M_SITE_DEFAULT,
                    nprocs=nprocs, verbose=1, log=None, dryrun=False)

    p = optparse.OptionParser(usage)
    p.set_defaults(**defaults)

    p.add_option("-T", "--topdir",
                 help="Specify the topdir of which VM building scripts "
                      "are [%default]")
    p.add_option("-s", "--site",
                 help="Specify the site target VM belongs to [%default]")
    p.add_option("-N", "--nprocs", type="int",
                 help="Number of parallel build jobs to run when building "
                      "multiple VMs. %prog will be forced to run all VM "
                      "building jobs sequentially if this option is set "
                      "to 1. [%default]")
    p.add_option("-v", "--verbose", action="store_const", const=0,
                 dest="verbose", help="Verbose mode")
    p.add_option("-q", "--quiet", action="store_const", const=2,
                 dest="verbose", help="Quiet mode")
    p.add_option("-L", "--log", help="Specify log file")
    p.add_option("", "--dryrun", action="store_true", help="Dry run mode")

    return p


def main(argv=sys.argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    set_loglevel(options.verbose)

    if not args:
        p.print_usage()
        sys.exit(0)

    if args[0] == "all":
        vms = list_all_vm_for_site(options.topdir, options.site)
    else:
        vms = args

    if len(vms) == 1:
        build_
        build_vm(vms[0], options.topdir, options.site, options.verbose > 0,
                 options.log, options.dryrun)
    else:
        build_vms(vms, options.nprocs, options.topdir, options.site,
                  options.verbose > 0, options.log, options.dryrun)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

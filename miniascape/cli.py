#
# Copyright (C) 2012, 2013 Satoru SATOH <ssato@redhat.com>
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
    M_GUESTS_CONF_SUBDIR

import miniascape.config as C
import miniascape.guest as G
import miniascape.options as O
import miniascape.utils as U
import miniascape.host as H
import miniascape.site as S

import datetime
import glob
import multiprocessing
import subprocess
import sys


def timestamp():
    return datetime.datetime.now().strftime("%F_%T")


def cmd2prog(c):
    return "miniascape " + c


def build_vm_cmd(name, workdir):
    """
    :param name: VM's name
    :param workdir: Working dir where vm build scripts exist
    """
    bindir = os.path.join(workdir, M_GUESTS_CONF_SUBDIR, name)
    bin = os.path.join(bindir, "vmbuild.sh")
    logfile = os.path.join(bindir, "vmbuild.%s.log" % timestamp())

    return "bash -x %s 2>&1 | tee %s" % (bin, logfile)


def build_vm(name, workdir, dryrun=True):
    """
    :param name: VM's name
    :param workdir: Working dir where vm build scripts exist
    :param dryrun: Just return command to run if True
    """
    c = build_vm_cmd(name, workdir)
    logging.info("Build vm: " + c)

    if dryrun:
        return True

    return subprocess.check_call(c, shell=True)


def build_vm_0(nwd):
    return build_vm(*nwd)


def gen_all(argv):
    p = H.option_parser()
    (options, args) = p.parse_args(argv)

    options = O.tweak_tmpldir(options)
    set_loglevel(options.verbose)

    cf = C.ConfFiles(options.confdir)

    H.gen_host_files(cf, options.tmpldir, options.workdir, options.force)
    G.gen_all(cf, options.tmpldir, options.workdir)


def build_all_vms(argv):
    p = H.option_parser()
    (options, args) = p.parse_args(argv)

    options = O.tweak_tmpldir(options)
    set_loglevel(options.verbose)

    cf = C.ConfFiles(options.confdir)

    vms = [os.path.basename(f) for f in
           glob.glob(os.path.join(options.workdir, M_GUESTS_CONF_SUBDIR, '*'))]

    if not vms:
        logging.error("No vms found. Aborting...")
        sys.exit(-1)

    pool = multiprocessing.Pool(multiprocessing.cpu_count() * 2)
    res = pool.map_async(build_vm_0, [(n, options.workdir, options.dryrun) for
                                      n in vms])
    pool.close()
    pool.join()


# TODO: define other commands.
cmds = [
    #("i", "init", H.main),
    ("c",  "configure", S.main,
     "Generate site configuration from config src"),
    ("ge", "generate", gen_all,
     "Generate all files to build guests and virt. infra"),
    ("gu", "guest", G.main, "Generate files to build specific guest"),
    ("b", "build", build_all_vms, "Build all VMs"),
]


def usage(prog, cmds=cmds):
    cs = "\n".join("\t%s (abbrev: %s)\t%s" % (c, a, h) for a, c, _f, h in cmds)
    print """Usage: %s COMMAND_OR_COMMAND_ABBREV [Options] [Arg ...]

Commands:
  %s
""" % (prog, cs)


def main(argv=sys.argv):
    assert not U.is_superuser(), \
           "Danger! You should NOT run this program as root!"

    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        usage(argv[0])
    else:
        cfs = [
            (c, f) for abbrev, c, f, _h in cmds if argv[1].startswith(abbrev)
        ]
        if cfs:
            (c, f) = cfs[0]
            f([cmd2prog(c)] + argv[2:])
        else:
            usage(argv[0])


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

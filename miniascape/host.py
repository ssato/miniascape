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
import miniascape.guest as MG
import miniascape.options as O
import miniascape.template as T
import miniascape.utils as U

import glob
import logging
import optparse
import os.path
import os
import sys
import yaml

from itertools import groupby
from operator import itemgetter


_NET_SUBDIR = "networks.d"
_HOST_SUBDIR = "host"


def _netoutdir(topdir):
    """
    :param topdir: Working top dir
    """
    return os.path.join(topdir, _HOST_SUBDIR, _NET_SUBDIR)


def _netconfdir(confdir):
    """
    :param confdir: Config topdir
    """
    return os.path.join(confdir, _NET_SUBDIR)


def aggregate_guest_networks(confdir):
    """
    Aggregate guest's network interface info from each guest configurations and
    return list of host list grouped by each networks.
    """
    gcs = MG.load_guests_confs(confdir)
    kf = itemgetter("network")
    hostsets = (
        (k, list(g)) for k, g in groupby(
            sorted(U.concat(g.get("interfaces", []) for g in gcs), key=kf), kf
        )
    )
    return hostsets


def find_dups(hosts, keys):
    seens = dict((k, {}) for k in keys)

    for h in hosts:
        for k in keys:
            x = h.get(k, None)
            if x is not None:
                xs = seens[k].get(x, [])
                if xs:
                    seens[k][x].append(h)
                else:
                    seens[k][x] = [h]

    for k in keys:
        for x, hs in seens[k].iteritems():
            if len(hs) > 1:  # duplicated entries
                yield (k, x, hs)


def check_dups_by_ip_and_mac(hosts):
    """
    Check if duplicated IP or MAC found in host list and warns about them.
    """
    for k, x, hs in find_dups(hosts, ("ip", "mac")):
        logging.warn(
            "Duplicated entries: key=%s, x=%s, hosts=%s" % \
                (k, x, ", ".join(h.get("host", str(h)) for h in hs))
        )


def load_configs(confdir):
    hostsets = dict(aggregate_guest_networks(confdir))

    nets = dict()
    nconfs = glob.glob(os.path.join(_netconfdir(confdir), "*.yml"))

    for nc in nconfs:
        netctx = T.load_confs([nc])
        name = netctx["name"]

        hosts = hostsets.get(name, [])
        if hosts:
            check_dups_by_ip_and_mac(hosts)
            netctx["hosts"] = hosts

        nets[name] = netctx

    return nets


def filterout_hosts_wo_macs(netconf):
    nc = yaml.load(open(netconf))
    nc["hosts"] = [h for h in nc.get("hosts", []) if "mac" in h]
    return nc


def _find_template(tmpldirs, template):
    for tdir in tmpldirs:
        tmpl = os.path.join(tdir, template)
        if os.path.exists(tmpl):
            return tmpl

    logging.warn(
        "Could not find template %s in paths: %s" % \
            (template, str(tmpldirs))
    )
    return template  # Could not find in tmpldirs


def gen_vnet_files(tmpldirs, confdir, workdir, force):
    nets = load_configs(confdir)
    outdir = _netoutdir(workdir)

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for name in nets:
        netconf = os.path.join(outdir, "%s.yml" % name)
        if os.path.exists(netconf) and not force:
            logging.warn("Net conf already exists: " + netconf)
            return

        yaml.dump(nets[name], open(netconf, 'w'))

        netxml = os.path.join(outdir, "%s.xml" % name)
        if os.path.exists(netxml) and not force:
            logging.warn("Net xml already exists: " + netxml)
            return

        logging.debug("Generating network xml: " + netxml)
        nc = filterout_hosts_wo_macs(netconf)
        tpaths = [os.path.join(d, "host") for d in tmpldirs]
        T.renderto(
            tpaths, nc, _find_template(tmpldirs, "host/network.xml"), netxml
        )

    T.renderto(
        tpaths, {"networks": [n for n in nets]},
        _find_template(tmpldirs, "host/network_register.sh"),
        os.path.join(outdir, "network_register.sh")
    )


def host_confs(confdir):
    """
    :param confdir: Config topdir
    :param name: Guest's name
    :return: Guest's config files (path pattern)
    """
    d = os.path.join(confdir, "host.d")

    assert os.path.exists(d), "Could not find host's confdir under " + confdir
    return os.path.join(d, "*.yml")


def gen_host_files(tmpldirs, confdir, workdir, force):
    conf =  T.load_confs([MG.common_confs(confdir), host_confs(confdir)])
    gen_vnet_files(tmpldirs, confdir, workdir, force)

    for k, v in conf.get("host_templates", {}).iteritems():
        (src, dst) = (v.get("src", None), v.get("dst", None))

        if src is None or dst is None:
            continue

        if os.path.sep in src:
            srcdirs = [os.path.join(d, os.path.dirname(src)) for d in tmpldirs]
        else:
            srcdirs = tmpldirs

        # strip dir part as it will be searched from srcdir.
        src = os.path.basename(src)
        dst = os.path.join(workdir, dst)

        logging.info("Generating %s from %s [%s]" % (dst, src, k))
        T.renderto(srcdirs + [workdir], conf, src, dst)


def option_parser():
    defaults = dict(force=False, yes=False, **O.M_DEFAULTS)
    p = O.option_parser(defaults, "%prog [OPTION ...]")

    p.add_option("-f", "--force", action="store_true",
        help="Force outputs even if these exist"
    )
    p.add_option("-y", "--yes", action="store_true",
        help="Assume yes for all Questions"
    )
    return p


def main(argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    U.init_log(options.verbose)
    options = O.tweak_tmpldir(options)

    houtdir = os.path.join(options.workdir, _HOST_SUBDIR)
    if os.path.exists(houtdir) and not options.yes:
        yesno = raw_input(
            "Are you sure to generate networks in %s ? [y/n]: " % \
                options.workdir
        )
        if not yesno.strip().lower().startswith('y'):
            print >> "Cancel creation of networks..."
            sys.exit(0)

    gen_host_files(
        options.tmpldir, options.confdir, options.workdir, options.force
    )


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

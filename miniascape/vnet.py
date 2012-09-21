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

import miniascape.guest as MG
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


def aggregate_guest_networks(confdir):
    """
    Aggregate guest's network interface info from each guest configurations and
    return list of host list grouped by each networks.
    """
    gcs = MG.load_guests_confs(confdir)
    kf = itemgetter("network")
    hostsets = (
        list(g) for k, g in groupby(
            sorted(U.concat(g.get("interfaces", []) for g in gcs), key=kf), kf
        )
    )
    return hostsets


def dup_check(hosts):
    ip_seen = {}
    mac_seen = {}

    for h in hosts:
        ip = h.get("ip", None)
        if ip is not None:
            ips = ip_seen.get(ip, [])
            if ips:
                logging.warn("Duplicated IP address in " + str(h))
                ip_seen[ip].append(h)
            else:
                ip_seen[ip] = [h]

        mac = h.get("mac", None)
        if mac is not None:
            ms = mac_seen.get(mac, [])
            if ms:
                logging.warn("Duplicated MAC address in " + str(h))
                mac_seen[mac].append(h)
            else:
                mac_seen[mac] = [h]
            

def load_configs(confdir):
    hostsets = aggregate_guest_networks(confdir)

    nets = dict()
    nconfs = glob.glob(os.path.join(confdir, "networks.d/*.yml"))

    for nc in nconfs:
        netctx = T.load_confs([nc])
        name = netctx["name"]

        hss = [hs for hs in hostsets if hs and hs[0]["network"] == name]
        if hss:
            dup_check(hss[0])
            netctx["hosts"] = hss[0]

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
    outdir = os.path.join(workdir, "host/networks.d")

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


def option_parser(argv=sys.argv, defaults=None):
    if defaults is None:
        defaults = dict(
            tmpldir=[], confdir=M_CONF_DIR, workdir=M_WORK_TOPDIR,
            force=False, yes=False, debug=False,
        )

    p = optparse.OptionParser("%prog [OPTION ...]", prog=argv[0])
    p.set_defaults(**defaults)

    p.add_option("-t", "--tmpldir", action="append", 
        help="Template top dirs [[%s]]" % M_TMPL_DIR
    )
    p.add_option("-c", "--confdir",
        help="Configuration files top dir [%default]"
    )
    p.add_option("-w", "--workdir", help="Working top dir [%default]")
    p.add_option("-f", "--force", action="store_true",
        help="Force outputs even if these exist"
    )
    p.add_option("-y", "--yes", action="store_true", default=False,
        help="Assume yes for all Questions"
    )
    p.add_option("-D", "--debug", action="store_true", help="Debug mode")

    return p


def main(argv):
    p = option_parser(argv)
    (options, args) = p.parse_args(argv[1:])

    U.init_log(options.debug)

    if not args or not options.yes:
        yesno = raw_input(
            "Are you sure to generate networks in %s ? [y/n]: " % \
                options.workdir
        )
        if not yesno.strip().lower().startswith('y'):
            print >> "Cancel creation of networks..."
            sys.exit(0)

    # System template path is always appended to the tail of search list.
    options.tmpldir.append(M_TMPL_DIR)

    gen_vnet_files(
        options.tmpldir, options.confdir, options.workdir, options.force
    )


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

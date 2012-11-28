#
# Copyright (C) 2012 Satoru SATOH <ssato at redhat.com>
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
from miniascape.globals import M_METACONF_DIR
from itertools import groupby
from operator import itemgetter

import miniascape.template as T
import miniascape.utils as U

import logging
import os.path
import os


_CATEGORIES = ("guest", "network", "storage")


def load_metaconfs(metaconfsrc=M_METACONF_DIR, categories=_CATEGORIES):
    """
    Load meta config for miniascape.
    """
    if os.path.isdir(metaconfsrc):
        metaconfdir = metaconfsrc
        confs = U.sglob(os.path.join(metaconfsrc, "*.yml"))
    else:
        metaconfdir = os.path.dirname(metaconfsrc)
        confs = [metaconfsrc]  # It's not a dir, just a file.

    d = T.load_confs(confs)

    confdir = os.path.abspath(os.path.join(metaconfdir, "..", d["site"]))
    d["confdir"] = confdir

    for c in categories:
        d[c]["dir"] = os.path.join(confdir, d[c]["subdir"])
        d[c]["confs"] = [os.path.join(confdir, p) for p in d[c]["files"]]

    return d


def load_guest_confs(metaconf, name):
    """
    :param metaconf: Meta conf object (:: dict) initialized by load_metaconfs.
    :param name: Guest's name
    """
    confs = [
        (p % {"name": name} if "%(" in p else p) for p in
            metaconf["guest"]["confs"]
    ]

    logging.info("Loading guest config files: " + name)
    return T.load_confs(confs)


def list_guest_names(metaconf):
    """
    :param metaconf: Meta conf object (:: dict) initialized by load_metaconfs.
    """
    return U.list_dirnames(os.path.join(metaconf["guest"]["dir"]))


def load_guests_confs(metaconf):
    """
    :param metaconf: Meta conf object (:: dict) initialized by load_metaconfs.
    """
    return [load_guest_confs(metaconf, n) for n in list_guest_names(metaconf)]


def list_net_names(metaconf):
    """
    :param metaconf: Meta conf object (:: dict) initialized by load_metaconfs.
    """
    return sorted(
        os.path.basename(x) for x in
            os.path.join(metaconf["network"]["dir"], "*.yml")
    )


def list_nets_confs(metaconf):
    return [
        [(p % {"name": n} if "%(" in p else p) for p in
            metaconf["network"]["confs"]
        ] for n in list_net_names(metaconf)
    ]


def _aggregate_guest_net_interfaces_g(metaconf):
    """
    Aggregate guest's network interface info from each guest configurations and
    return list of host list grouped by each networks.

    :param metaconf: Meta conf object (:: dict) initialized by load_metaconfs.
    """
    gcs = load_guests_confs(metaconf)
    kf = itemgetter("network")
    return (
        (k, list(g)) for k, g in groupby(
            sorted(U.concat(g.get("interfaces", []) for g in gcs), key=kf), kf
        )
    )


def _check_dups_by_ip_or_mac(nis):
    """
    Check if duplicated IP or MAC found in host list and warns about them.

    :param nis: A list of network interfaces, {ip, mac, ...}
    """
    for k, v, ns in U.find_dups_in_dicts_list_g(nis, ("ip", "mac")):
        logging.warn(
            "Duplicated entries: key=%s, v=%s, hosts=%s" % \
                (k, v, ", ".join(n.get("host", str(n)) for n in ns))
        )


def load_nets_confs(metaconf):
    nets = dict()
    ncss = list_nets_confs(metaconf)
    nis = dict(_aggregate_guest_net_interfaces_g(metaconf))

    for ncs in ncss:
        netctx = T.load_confs(ncs)
        name = netctx["name"]

        ns = nis.get(name, [])
        if ns:
            _check_dups_by_ip_or_mac(ns)
            netctx["hosts"] = ns

        nets[name] = netctx

    return nets


def host_confs(metaconf):
    """
    :param metaconf: Meta conf object (:: dict) initialized by load_metaconfs.
    :return: Guest's config files (path pattern)
    """
    d = os.path.join(metaconf["confdir"], "host.d")

    assert os.path.exists(d), "Could not find host's confdir under " + confdir
    return os.path.join(d, "*.yml")


# vim:sw=4:ts=4:et:

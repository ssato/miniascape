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
import anyconfig as AC

import datetime
import logging
import os.path
import os
import re


_CATEGORIES = ("guest", "network", "host")


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


def _timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def add_special_confs(conf):
    """
    :param conf: Configurations :: dict

    >>> conf = add_special_confs(dict())

    >>> assert "miniascape" in conf, str(conf)
    >>> assert "build" in conf["miniascape"], str(conf)
    >>> assert "user" in conf["miniascape"]["build"], str(conf)
    >>> assert "host" in conf["miniascape"]["build"], str(conf)
    >>> assert "time" in conf["miniascape"]["build"], str(conf)
    >>> assert "builder" in conf["miniascape"], str(conf)
    """
    diff = dict(build=dict(user=U.get_username(),
                           host=U.get_hostname(fqdn=False),
                           time=_timestamp()))

    diff["builder"] = "%(user)s@%(host)s" % diff["build"]

    conf["miniascape"] = diff

    return conf


def load_metaconfs(metaconfsrc=M_METACONF_DIR, categories=_CATEGORIES):
    """
    Load meta config for miniascape.
    """
    if os.path.isdir(metaconfsrc):
        metaconfdir = metaconfsrc
        conf = AC.load(os.path.join(metaconfsrc, "*.yml"), merge=AC.MS_DICTS)
    else:
        metaconfdir = os.path.dirname(metaconfsrc)
        conf = AC.load(metaconfsrc, merge=AC.MS_DICTS)

    confdir = os.path.abspath(os.path.join(metaconfdir, "..", conf["site"]))
    conf["confdir"] = confdir

    for c in categories:
        conf[c]["dir"] = os.path.join(confdir, conf[c]["subdir"])
        conf[c]["confs"] = [os.path.join(confdir, p) for p in conf[c]["files"]]

    return conf


def load_guest_confs(metaconf, name):
    """
    :param metaconf: Meta conf object (:: dict) initialized by load_metaconfs.
    :param name: Guest's name
    """
    confs = [
        (p % {"name": name, "group": _sysgroup(name)} if "%(" in p else p) \
            for p in metaconf["guest"]["confs"]
    ]

    logging.info("Loading guest config files: " + name)
    c = AC.load(confs, merge=AC.MS_DICTS)

    return add_special_confs(c)


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
    :param metaconf: Meta conf object.
    """
    return U.list_dirnames(os.path.join(metaconf["network"]["dir"]))


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
        netctx = AC.load(ncs, merge=AC.MS_DICTS)
        name = netctx["name"]

        ns = nis.get(name, [])
        if ns:
            _check_dups_by_ip_or_mac(ns)
            netctx["hosts"] = ns

        nets[name] = netctx

    return nets


def load_host_confs(metaconf):
    """
    :param metaconf: Meta conf object.
    """
    logging.info("Loading host config files")
    return AC.load(metaconf["host"]["confs"], merge=AC.MS_DICTS)


# vim:sw=4:ts=4:et:

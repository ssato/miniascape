#
# Copyright (C) 2012 - 2018 Satoru SATOH <ssato at redhat.com>
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
from miniascape.globals import LOGGER as logging

import anyconfig
import itertools
import os.path

import miniascape.globals as G
import miniascape.memoize
import miniascape.utils as U


def list_net_names(netdir):
    """
    :param netdir: Networks' conf dir, e.g. /etc/miniascape/default/networks.d
    """
    return U.list_dirnames(netdir)


def list_group_and_guests_g(guestdir):
    """
    :param guestdir: Guests' config dir, e.g. /etc/miniascape/default/guests.d
    :return: (group :: str, guest_name :: str) (generator)
    """
    for group in U.list_dirnames(guestdir):
        for guest in U.list_dirnames(os.path.join(guestdir, group)):
            yield (group, guest)


def _find_group_of_guest(name, guestdir):
    """
    :param guestdir: Guests' config dir, e.g. /etc/miniascape/default/guests.d
    :return: group :: str
    """
    for g, n in list_group_and_guests_g(guestdir):
        if n == name:
            return g

    return None


find_group_of_guest = miniascape.memoize.memoize(_find_group_of_guest)


def _add_special_confs(conf):
    """
    :param conf: Configurations :: dict

    >>> conf = _add_special_confs(dict())

    >>> assert "miniascape" in conf, str(conf)
    >>> assert "build" in conf["miniascape"], str(conf)
    >>> assert "user" in conf["miniascape"]["build"], str(conf)
    >>> assert "host" in conf["miniascape"]["build"], str(conf)
    >>> assert "time" in conf["miniascape"]["build"], str(conf)
    >>> assert "builder" in conf["miniascape"], str(conf)
    """
    diff = dict(build=dict(user=U.get_username(),
                           host=U.get_hostname(fqdn=False),
                           time=G.timestamp("%Y%m%d_%H%M%S")))
    diff["builder"] = "{user}s@{host}".format(**diff["build"])
    conf["miniascape"] = diff

    return conf


def _guest_add_missings(conf):
    assert "hostname" in conf, \
        "You must specify 'hostname' for guests at least: " + str(conf)

    if "hostname" not in conf:
        conf["hostname"] = conf["name"]

    if "domain" in conf:
        if "fqdn" not in conf:
            conf["fqdn"] = "{hostname}.{domain}".format(**conf)

    # TODO: Automatic (static) dhcp address assignment:
    # if conf.get("ip", None) == "auto":
    #    ...

    nics = conf.get("interfaces", [])
    nnics = len(nics)

    if nnics == 1:
        eth0 = nics[0]

        # see the description of 'mac' assignment in virt-install(1):
        if "mac" not in eth0:
            conf["interfaces"][0]["mac"] = "RANDOM"

        for k in ("hostname", "fqdn", "ip"):
            if k not in eth0 and k in conf:
                conf["interfaces"][0][k] = conf[k]

        if "device" not in eth0:
            conf["interfaces"][0]["device"] = "eth0"

    elif nnics > 1:
        for i in range(0, nnics):
            if "mac" not in nics[i]:
                conf["interfaces"][i]["mac"] = "RANDOM"

            if "device" not in nics[i]:
                conf["interfaces"][i]["device"] = "eth{}".format(i)

    return conf


def _ignorable_kv_pair(k, v):
    return k == "mac" and v == "RANDOM"


def _check_dups_by_ip_or_mac(nis):
    """
    Check if duplicated IP or MAC found in host list and warns about them.

    :param nis: A list of network interfaces, {ip, mac, ...}
    """
    for k, v, ns in U.find_dups_in_dicts_list_g(nis, ("ip", "mac")):
        if _ignorable_kv_pair(k, v):
            continue

        m = "Duplicated entries: key={}, v={}, hosts={}"
        logging.warn(m.format(k, v, ", ".join(n.get("host", str(n)) for n
                                              in ns)))


class ConfFiles(dict):

    def __init__(self, confdir=G.M_CONFDIR_DEFAULT,
                 common_subdir=G.M_COMMON_CONF_SUBDIR,
                 guest_subdir=G.M_GUESTS_CONF_SUBDIR,
                 net_subdir=G.M_NETS_CONF_SUBDIR,
                 host_subdir=G.M_HOST_CONF_SUBDIR,
                 pattern=G.M_CONF_PATTERN):
        """
        :param confdir: Site config top dir, e.g. /etc/miniascape.d/default
        """
        self.confdir = confdir
        self.commondir = os.path.join(confdir, common_subdir)
        self.guestdir = os.path.join(confdir, guest_subdir)
        self.netdir = os.path.join(confdir, net_subdir)
        self.hostdir = os.path.join(confdir, host_subdir)
        self.pattern = pattern

    def list_guest_names(self):
        return list(n for _g, n in list_group_and_guests_g(self.guestdir))

    def list_host_confs(self):
        return [os.path.join(self.commondir, self.pattern),
                os.path.join(self.hostdir, self.pattern)]

    def list_guest_confs(self, name, group=None):
        """
        :param name: Guest's name, e.g. satellite-1
        :param group: Guest's group or None, e.g. satellite
        """
        if group is None:
            group = find_group_of_guest(name, self.guestdir)

        return [os.path.join(self.commondir, self.pattern),
                os.path.join(self.guestdir, group, self.pattern),
                os.path.join(self.guestdir, group, name, self.pattern)]

    def list_net_confs(self, name):
        """
        :param name: Net's name
        """
        return [os.path.join(self.commondir, self.pattern),
                os.path.join(self.netdir, self.pattern),
                os.path.join(self.netdir, name, self.pattern)]

    def list_nets_confs(self):
        return [self.list_net_confs(n) for n in list_net_names(self.netdir)]

    def load_host_confs(self):
        confs = self.list_host_confs()

        logging.info("Loading host configs")
        return anyconfig.load(confs, ac_template=True)

    def load_guest_confs(self, name, group=None):
        """
        :param name: Guest's name, e.g. satellite-1
        :param group: Guest's group, e.g. satellite
        """
        confs = self.list_guest_confs(name, group)

        logging.info("Loading guest configs: %s", name)
        c = anyconfig.load(confs, ac_template=True)

        return _add_special_confs(_guest_add_missings(c))

    def load_guests_confs(self):
        """
        Load all guests' config files.

        :return: [guest_conf :: dict]
        """
        return [self.load_guest_confs(n, g) for g, n in
                list_group_and_guests_g(self.guestdir)]

    def _aggregate_guest_net_interfaces_g(self):
        """
        Aggregate guest's network interface info from each guest configurations
        and return list of host list grouped by each networks.
        """
        gcs = self.load_guests_confs()
        kf = lambda d: d.get("network", False)
        return ((k, list(g)) for k, g in
                itertools.groupby(sorted(filter(bool,
                                                U.concat(g.get("interfaces",
                                                               []) for g
                                                         in gcs)),
                                         key=kf), kf))

    def load_nets_confs(self):
        nets = dict()

        ncss = self.list_nets_confs()
        nis = dict(self._aggregate_guest_net_interfaces_g())

        for ncs in ncss:
            netctx = anyconfig.load(ncs, ac_template=True)
            name = netctx["name"]

            ns = nis.get(name, [])
            if ns:
                _check_dups_by_ip_or_mac(ns)
                netctx["hosts"] = ns

            nets[name] = netctx

        return nets

# vim:sw=4:ts=4:et:

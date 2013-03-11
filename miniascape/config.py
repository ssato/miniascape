#
# Copyright (C) 2012, 2013 Satoru SATOH <ssato at redhat.com>
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
from miniascape.globals import M_CONFDIR_DEFAULT, M_COMMON_CONF_SUBDIR, \
    M_COMMON_CONF_SUBDIR, M_GUESTS_CONF_SUBDIR, M_NETS_CONF_SUBDIR, \
    M_HOST_CONF_SUBDIR, M_CONF_PATTERN
from itertools import groupby
from operator import itemgetter

import miniascape.memoize as M
import miniascape.template as T
import miniascape.utils as U
import anyconfig as AC

import datetime
import logging
import os.path
import os
import re


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


def list_net_names(confdir=M_CONFDIR_DEFAULT,
                   subdir=M_NETS_CONF_SUBDIR):
    """
    :param confdir: Site config top dir, e.g. /etc/miniascape.d/default
    :param subdir: Config sub dir, e.g. guests.d
    """
    return U.list_dirnames(os.path.join(confdir, subdir))


def list_group_and_guests_g(confdir=M_CONFDIR_DEFAULT,
                            subdir=M_GUESTS_CONF_SUBDIR):
    """
    :param confdir: Site config top dir, e.g. /etc/miniascape.d/default
    :param subdir: Config sub dir, e.g. guests.d
    :return: (group, guest_name)
    """
    guestsdir = os.path.join(confdir, subdir)

    for group in U.list_dirnames(guestsdir):
        for guest in U.list_dirnames(os.path.join(guestsdir, group)):
            yield (group, guest)


def list_guest_confs(group, name, confdir=M_CONFDIR_DEFAULT,
                     common_subdir=M_COMMON_CONF_SUBDIR,
                     subdir=M_GUESTS_CONF_SUBDIR,
                     pattern=M_CONF_PATTERN):
    """
    :param group: Guest's group, e.g. satellite
    :param name: Guest's name, e.g. satellite-1
    :param confdir: Site config top dir, e.g. /etc/miniascape.d/default
    """
    return [os.path.join(confdir, common_subdir, pattern),
            os.path.join(confdir, subdir, group, pattern),
            os.path.join(confdir, subdir, group, name, pattern), ]


def list_net_confs(name, confdir=M_CONFDIR_DEFAULT,
                   common_subdir=M_COMMON_CONF_SUBDIR,
                   subdir=M_NETS_CONF_SUBDIR,
                   pattern=M_CONF_PATTERN):
    """
    :param name: Net's name
    :param confdir: Site config top dir, e.g. /etc/miniascape.d/default
    """
    return [os.path.join(confdir, common_subdir, pattern),
            os.path.join(confdir, subdir, pattern),
            os.path.join(confdir, subdir, name, pattern), ]


def list_host_confs(confdir=M_CONFDIR_DEFAULT,
                    common_subdir=M_COMMON_CONF_SUBDIR,
                    subdir=M_NETS_CONF_SUBDIR,
                    pattern=M_CONF_PATTERN):
    """
    :param confdir: Site config top dir, e.g. /etc/miniascape.d/default
    """
    return [os.path.join(confdir, common_subdir, pattern),
            os.path.join(confdir, subdir, pattern), ]


def list_nets_confs(confdir=M_CONFDIR_DEFAULT,
                    common_subdir=M_COMMON_CONF_SUBDIR,
                    subdir=M_NETS_CONF_SUBDIR,
                    pattern=M_CONF_PATTERN):
    return [
        list_net_confs(n, confdir, common_subdir, subdir, pattern) for n in
        list_net_names(confdir, subdir)
    ]


def _find_group_of_guest(name, confdir=M_CONFDIR_DEFAULT,
                        subdir=M_GUESTS_CONF_SUBDIR):
    """
    :param confdir: Site config top dir, e.g. /etc/miniascape.d/default
    :param subdir: Config sub dir, e.g. guests.d
    :return: group :: str
    """
    for g, n in list_group_and_guests_g(confdir, subdir):
        if n == name:
            return g

    return None


find_group_of_guest = M.memoize(_find_group_of_guest)


def load_guest_confs(name, group=None, confdir=M_CONFDIR_DEFAULT,
                     common_subdir=M_COMMON_CONF_SUBDIR,
                     subdir=M_GUESTS_CONF_SUBDIR,
                     pattern=M_CONF_PATTERN):
    """
    :param name: Guest's name, e.g. satellite-1
    :param group: Guest's group, e.g. satellite
    :param confdir: Site config top dir, e.g. /etc/miniascape.d/default
    """
    if group is None:
        group = find_group_of_guest(name, confdir, subdir)

    confs = list_guest_confs(group, name, confdir, common_subdir, subdir,
                             pattern)

    logging.info("Loading guest config files: " + name)
    c = AC.load(confs, merge=AC.MS_DICTS)

    return add_special_confs(c)


def load_host_confs(confdir=M_CONFDIR_DEFAULT,
                    common_subdir=M_COMMON_CONF_SUBDIR,
                    subdir=M_HOST_CONF_SUBDIR,
                    pattern=M_CONF_PATTERN):
    """
    :param confdir: Site config top dir, e.g. /etc/miniascape.d/default
    """
    confs = list_host_confs(confdir, common_subdir, subdir, pattern)

    logging.info("Loading host config files")
    return AC.load(confs, merge=AC.MS_DICTS)


def load_guests_confs(confdir=M_CONFDIR_DEFAULT,
                      common_subdir=M_COMMON_CONF_SUBDIR,
                      subdir=M_GUESTS_CONF_SUBDIR,
                      pattern=M_CONF_PATTERN):
    """
    :param name: Guest's name
    :param confdir: Site config top dir, e.g. /etc/miniascape.d/default
    """
    return [
        load_guest_confs(n, g, confdir, common_subdir, subdir, pattern)
        for g, n in list_group_and_guests_g(confdir, subdir)
    ]


def _aggregate_guest_net_interfaces_g(confdir=M_CONFDIR_DEFAULT,
                                      common_subdir=M_COMMON_CONF_SUBDIR,
                                      subdir=M_GUESTS_CONF_SUBDIR,
                                      pattern=M_CONF_PATTERN):
    """
    Aggregate guest's network interface info from each guest configurations and
    return list of host list grouped by each networks.

    :param name: Guest's name
    :param confdir: Site config top dir, e.g. /etc/miniascape.d/default
    """
    gcs = load_guests_confs(confdir, common_subdir, subdir, pattern)
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
            "Duplicated entries: key=%s, v=%s, hosts=%s" %
            (k, v, ", ".join(n.get("host", str(n)) for n in ns))
        )


def load_nets_confs(confdir=M_CONFDIR_DEFAULT,
                    common_subdir=M_COMMON_CONF_SUBDIR,
                    guest_subdir=M_GUESTS_CONF_SUBDIR,
                    net_subdir=M_NETS_CONF_SUBDIR,
                    pattern=M_CONF_PATTERN):
    nets = dict()
    ncss = list_nets_confs(confdir, common_subdir, net_subdir, pattern)
    nis = dict(_aggregate_guest_net_interfaces_g(confdir, common_subdir,
                                                 guest_subdir, pattern))

    for ncs in ncss:
        netctx = AC.load(ncs, merge=AC.MS_DICTS)
        name = netctx["name"]

        ns = nis.get(name, [])
        if ns:
            _check_dups_by_ip_or_mac(ns)
            netctx["hosts"] = ns

        nets[name] = netctx

    return nets


# vim:sw=4:ts=4:et:

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
from __future__ import print_function
from miniascape.globals import LOGGER as logging, set_loglevel

import miniascape.config as C
import miniascape.globals as G
import miniascape.options as O
import miniascape.template as T
import miniascape.utils as U

import anyconfig as A
import optparse
import os.path
import os
import sys


def _netxml_path(hsubdir=G.M_HOST_OUT_SUBDIR, subdir=G.M_NETS_OUT_SUBDIR,
                 netxml="network.xml"):
    return os.path.join(hsubdir, subdir, netxml)


def _netoutdir(topdir, host_subdir=G.M_HOST_OUT_SUBDIR,
               net_subdir=G.M_NETS_OUT_SUBDIR):
    """
    :param topdir: Working top dir

    >>> _netoutdir("/tmp/a", "host", "usr/share/miniascape/networks.d")
    '/tmp/a/host/usr/share/miniascape/networks.d'
    """
    return os.path.join(topdir, host_subdir, net_subdir)


def hosts_w_unique_ips(nc):
    """
    :return: list of hosts having nics w unique ip addresses assigned.

    >>> nc = dict(hosts=[dict(ip='192.168.122.10', ),
    ...                  dict(mac="RANDOM", ),
    ...                  dict(ip='192.168.122.21', )])
    >>> hosts_w_unique_ips(nc)
    [{'ip': '192.168.122.10'}, {'ip': '192.168.122.21'}]
    """
    return [h for h in nc.get("hosts", []) if "ip" in h]


def hosts_w_unique_macs(nc):
    """
    :return: list of hosts having nics w unique mac addresses assigned.

    >>> nc = dict(hosts=[dict(mac="RANDOM"),
    ...                  dict(mac="52:54:00:07:10:58"),
    ...                  dict(mac="52:54:00:07:10:59"),
    ...                  dict(mac="RANDOM")])
    >>> hosts_w_unique_macs(nc)
    [{'mac': '52:54:00:07:10:58'}, {'mac': '52:54:00:07:10:59'}]
    """
    return [h for h in nc.get("hosts", [])
            if "mac" in h and h["mac"] != "RANDOM"]


def _find_template(tmpldirs, template):
    for tdir in tmpldirs:
        tmpl = os.path.join(tdir, template)
        if os.path.exists(tmpl):
            return tmpl

    logging.warn("Could not find template %s in paths: %s" %
                 (template, str(tmpldirs)))
    return template  # Could not find in tmpldirs


def gen_vnet_files(cf, tmpldirs, workdir, force):
    """
    Generate libvirt network def. XML files.

    :param cf: An instance of miniascape.config.ConfFiles
    :param tmpldirs: Template search paths
    :param workdir: Working dir to save generated XML files
    :param force: Existing ones may be overwritten if True
    """
    nets = cf.load_nets_confs()
    outdir = _netoutdir(workdir)
    tmpl = _find_template(tmpldirs, _netxml_path())
    tpaths = [os.path.dirname(tmpl)]

    logging.debug("Network XML params: tpaths=%s, tmpl=%s" % (tpaths, tmpl))

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for name in nets:
        netconf = os.path.join(outdir, "%s.yml" % name)
        if os.path.exists(netconf) and not force:
            logging.warn("Net conf already exists: " + netconf)
            return

        logging.debug("Dump conf for the net: " + name)
        A.dump(nets[name], netconf)

        netxml = os.path.join(outdir, "%s.xml" % name)
        if os.path.exists(netxml) and not force:
            logging.warn("Net xml already exists: " + netxml)
            return

        nc = A.load(netconf)
        nc["hosts"] = hosts_w_unique_ips(nc)
        nc["hosts_w_unique_macs"] = hosts_w_unique_macs(nc)

        logging.debug("Generating network xml: " + netxml)
        T.renderto(tpaths, nc, tmpl, netxml)


def gen_host_files(cf, tmpldirs, workdir, force):
    """
    Generate files for libvirt host.

    :param cf: An instance of miniascape.config.ConfFiles
    :param tmpldirs: Template search paths
    :param workdir: Working dir to save generated XML files
    :param force: Existing ones may be overwritten if True
    """
    conf = cf.load_host_confs()
    gen_vnet_files(cf, tmpldirs, workdir, force)

    conf["timestamp"] = G.timestamp()
    T.compile_conf_templates(conf, tmpldirs, workdir, "host_templates")


def option_parser():
    defaults = dict(force=False, yes=False, dryrun=False,
                    confdir=G.site_confdir(), **O.M_DEFAULTS)

    p = O.option_parser(defaults, "%prog [OPTION ...]")
    p.add_option("-f", "--force", action="store_true",
                 help="Force outputs even if these exist")
    p.add_option("", "--dryrun", action="store_true", help="Dry run mode")
    p.add_option("-c", "--confdir",
                 help="Top dir to hold site configuration files or "
                      "configuration file [%default]")
    return p


def main(argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    set_loglevel(options.verbose)
    options = O.tweak_options(options)

    cf = C.ConfFiles(options.confdir)

    houtdir = os.path.join(options.workdir, G.M_HOST_CONF_SUBDIR)
    if os.path.exists(houtdir) and not options.force:
        yesno = raw_input(
            "Are you sure to generate networks in %s ? [y/n]: " %
            options.workdir
        )
        if not yesno.strip().lower().startswith('y'):
            print("Cancel creation of networks...")
            sys.exit(0)

        options.force = True

    gen_host_files(cf, options.tmpldir, options.workdir, options.force)


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

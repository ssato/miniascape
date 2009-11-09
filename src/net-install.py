#! /usr/bin/python
#
# install / uninstall libvirt network from network xml file.
#
# Copyright (C) 2009 Satoru SATOH <satoru.satoh at gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#
# @see http://libvirt.org/html/libvirt-libvirt.html
# @see http://libvirt.org/formatnetwork.html
#

import libvirt
import logging
import optparse
import sys

try:
    import xml.etree.ElementTree as ET  # python >= 2.5
except ImportError:
    import elementtree.ElementTree as ET  # python <= 2.4; needs ElementTree.



VMM = 'qemu:///system'
(NET_STATE_UNKNOWN, NET_NOT_DEFINED, NET_DEFINED, NET_ACTIVE) = (0, 1, 2, 3)



def name_from_netxml(netxml):
    """Extract network name from given network xml file.
    """
    name = ''
    try:
        tree = ET.parse(netxml)
        elem = tree.find('/network/name')
        if elem is not None:
            name = elem.text
        logging.debug("Network Name = '%s'" % name)

    except IOError:
        raise RuntimeError("Could not open '%s'" % netxml)

    except IndexError:
        raise RuntimeError("Parse failed: '%s'" % netxml)

    return name



def status(network_name):
    """Query the status of the network.
    """
    try:
        conn = libvirt.openReadOnly(None)

        if network_name in conn.listNetworks():
            ret = NET_ACTIVE
        elif network_name in conn.listDefinedNetworks():
            ret = NET_DEFINED
        else:
            ret = NET_NOT_DEFINED

    except libvirt.libvirtError:
        ret = NET_STATE_UNKNOWN

    return ret


class ActiveNetworkException(Exception): pass
class DefinedNetworkException(Exception): pass


# actions:
def do_check(network_name, *args):
    """Check the network defined.
    """
    return status(network_name)


def do_uninstall(network_name, network_xml, force, *args):
    """Uninstall the network.
    """
    stat = status(network_name)

    try:
        conn = libvirt.open(VMM)
    except libvirt.libvirtError:
        logging.warn("Could not connect to libvirtd")
        return False

    if stat == NET_ACTIVE or stat == NET_DEFINED:
        net = conn.networkLookupByName(network_name)

        if stat == NET_ACTIVE:
            if force:
                logging.debug("Try destroying the network '%s' ..." % network_name)
                net.destroy()
                logging.debug("... Done")
            else:
                raise ActiveNetworkException("Network '%s' is defined and active already." % network_name)

        logging.debug("Try undefining the network '%s' ..." % network_name)
        net.undefine()
        logging.debug("... Done")

    else:
        logging.warn("Netowrk '%s' is not defined. Nothing to do..." % network_name)
        return False

    return network_name not in conn.listNetworks() + conn.listDefinedNetworks()


def do_install(network_name, network_xml, force, autostart, *args):
    """Install the network.
    """
    try:
        conn = libvirt.open(VMM)
    except libvirt.libvirtError:
        logging.error("Could not connect to libvirtd")
        return False

    if force:
        do_uninstall(network_name, network_xml, force)
        # FIXME: Reopen connection closed.
        conn.close()
        conn = libvirt.open(VMM)

    conn.networkDefineXML(open(network_xml, 'r').read())
    # FIXME: Reopen connection. It seems needed to apply the changes above.
    conn.close()
    conn = libvirt.open(VMM)

    net = conn.networkLookupByName(network_name)

    if autostart:
        logging.debug("Making the network '%s' will be autostarted." % network_name)
        net.setAutostart(True)

    logging.debug("Starts the network '%s' just created." % network_name)
    net.create()

    return network_name in conn.listNetworks()


def option_parser():
    parser = optparse.OptionParser("%prog [OPTION ...] COMMAND NETWORK_XML\n\n"
        "Commands: install, uninstall, update\n")
    parser.add_option('-f', '--force', dest='force',
        action="store_true", default=False, help='Force action')
    parser.add_option('-v', '--verbose', dest='verbose', action="store_true",
        default=False, help='verbose mode')
    parser.add_option('-q', '--quiet', dest='quiet', action="store_true",
        default=False, help='quiet mode')

    iog = optparse.OptionGroup(parser, "Options for 'install'")
    iog.add_option('-a', '--autostart', action="store_true", default=False,
        help='Make the network autostarted after installed')
    parser.add_option_group(iog)

    return parser


def main():
    action = do_check
    loglevel = logging.INFO

    parser = option_parser()
    (options, args) = parser.parse_args()

    if options.verbose:
        loglevel = logging.DEBUG
    if options.quiet:
        loglevel = logging.WARN

    # logging.basicConfig() in python older than 2.4 cannot handle kwargs,
    # then exception 'TypeError' will be thrown.
    try:
        logging.basicConfig(level=loglevel)

    except TypeError:
        # To keep backward compatibility. See above comment also.
        logging.getLogger().setLevel(loglevel)

    if len(args) < 2:
        parser.print_help()
        sys.exit(1)

    if args[0].startswith('inst'):
        action = do_install
    if args[0].startswith('unin'):
        action = do_uninstall
    else:
        action = do_check

    network_xml = args[1]
    network_name = name_from_netxml(network_xml)

    ret = action(network_name, network_xml, options.force, options.autostart)
    sys.exit(ret)


if __name__ == '__main__':
    main()

# vim:sw=4:ts=4:et:ft=python:

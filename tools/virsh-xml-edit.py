#
# Copyright (C) 2012 Red Hat, Inc.
# Red Hat Author(s): Satoru SATOH <ssato@redhat.com>
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
import xml.etree.ElementTree as ET

import libvirt
import logging
import os
import sys


def create_etree(xmlfile):
    return ET.parse(open(xmlfile))


def find_xml_elem_by_xpath(etree, xpath):
    return etree.findall(xpath)


def libvirt_connect(readonly=True, connect=None):
    return (libvirt.openReadOnly if readonly else libvirt.open)(connect)


def is_libvirt_network_defined(conn, name):
    return conn.networkLookupByName(name) is not None


def libvirt_register_network(conn, xmlfile):
    name = create_etree(xmlfile).findtext(".//name")

    if is_libvirt_network_defined(conn, name):
        logging.warn("%s is already registered. Do nothing..." % name)
        return

    net = conn.networkDefineXML(xmlfile)
    if net is None:
        raise RuntimeError("Could not create a network from xml: " + xmlfile)

    rc = net.setAutostart(True)
    if rc != 0:
        logging.warn("Could not set autostart for the net: " + net.name())

    rc = net.create()
    if rc != 0:
        logging.warn("Could not create the net: " + net.name())


def add_host_into_network_xml(xmlfile, host):
    """
    @param xmlfile: Libvirt network xml file path
    @param host: {"name", "ip", "mac"}
    """
    tree = create_etree(xmlfile)
    hname = host["name"]

    dhcp_elem = find_xml_elem_by_xpath(tree, ".//ip/dhcp")
    if not dhcp_elem:
        logging.error("dhcp element does not found in the xml: " xmlfile)
        return

    if find_xml_elem_by_xpath(dhcp_elem, "host/[@name='%s']" % hname):
        logging.warn("The host '%s' already exists in the xml" % hname)
        return

    dhcp_elem.append(ET.Element("host", **host))

    dns_elem = find_xml_elem_by_xpath(tree, ".//dns")
    if not dns_elem:
        logging.error("dns element does not found in the xml: " xmlfile)
        return

    if not find_xml_elem_by_xpath(dns_elem, "host/[@ip='%s']" % host["ip"]):
        he = ET.Element("host", ip=host["ip"])
        hne = ET.Element("hostname")
        hne.text = host["name"]

        he.append(hne)
        dns_elem.append(he)

    tmpxmlfile = xmlfile + ".tmp"
    tree.write(tmpxmlfile)
    os.rename(tmpxmlfile, xmlfile)


def main(argv):
    pass


if __name__ == '__main__':
    main(sys.argv)

# vim:sw=4:ts=4:et:

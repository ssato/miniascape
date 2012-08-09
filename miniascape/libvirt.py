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
import miniascape.xml as X

import libvirt
import logging


def connect(readonly=True, connect=None):
    return (libvirt.openReadOnly if readonly else libvirt.open)(connect)


def is_network_defined(conn, name):
    return conn.networkLookupByName(name) is not None


def name_by_xml(xmlfile):
    return X.create_etree(xmlfile).findtext(".//name")


def register_network(conn, xmlfile):
    name = name_by_xml(xmlfile)

    if is_network_defined(conn, name):
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


def deregister_network(conn, name):
    net = conn.networkLookupByName(name)
    if not net:
        logging.warn("%s is not registered. Do nothing..." % name)
        return

    net.undefine()  # Do not stop it.


# vim:sw=4:ts=4:et:

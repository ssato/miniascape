#! /usr/bin/python
#
# Remvoe DHCP related stuff in libvirt network XML file.
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

import optparse
import sys

import xml.etree.ElementTree as ET  # python >= 2.5



def delete_dhcp_stuff(netxml, output):
    """@throw ExpatError - Invalid XML or not XML file.
    """
    assert netxml != output, "Input/output is the same file: '%s'" % netxml

    tree = ET.parse(netxml)

    ip = tree.find('ip')
    if ip is not None:
        [ip.remove(e) for e in ip.getiterator('dhcp')]

    if output is None or output == '-':
        output = sys.stdout
    else:
        output = open(output,'w')

    tree.write(output)


def option_parser():
    parser = optparse.OptionParser("%prog [OPTION ...] NETWORK_XML")
    parser.add_option('-o', '--output', default='-', help='output file [%default] (stdout)')
    return parser


def main():
    parser = option_parser()
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    network_xml = args[0]

    delete_dhcp_stuff(network_xml, options.output)



if __name__ == '__main__':
    main()

# vim:sw=4:ts=4:et:ft=python:

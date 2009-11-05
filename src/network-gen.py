#! /usr/bin/python
#
# Generate network service configs from libvirt network XML.
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

import logging
import optparse
import sys

import xml.etree.ElementTree as ET  # python >= 2.5

# future plan:
#from Cheetah.Template import Template


class ConfFmtr(object):
    def __init__(self, netxml):
        self._netxml = netxml
        self._tree = ET.parse(netxml)

    def find(self, path):
        return self._tree.find(path)

    def dump(self, output=None):
        assert self._netxml != output, "Output file is same as input: '%s'" % output

        if output is None:
            output = sys.stdout
        else:
            output = open(output,'w')

        self._tree.write(output)
        output.close()


class LibvirtConfFmtr(ConfFmtr):
    """
    """

    def __init__(self, netxml):
        ConfFmtr.__init__(self, netxml)

    def remove_hosts(self):
        """Removes host-ip-mac map elements in network XML.

        @see http://libvirt.org/formatnetwork.html
        """
        ip = self.find('//ip')
        [ip.remove(e) for e in ip.getiterator('host')]

    def remove_uuid(self):
        root = self._tree.getroot()
        [root.remove(e) for e in root.getiterator('uuid')]



class DnsmasqConfFmtr(ConfFmtr):
    """
    """
    def __init__(self, netxml):
        ConfFmtr.__init__(self, netxml)
        self._header = self.header()
        self._hosts = self.hosts()

    def dump(self, output=None):
        assert self._netxml != output, "Output file is same as input: '%s'" % output

        if output is None:
            output = sys.stdout
        else:
            output = open(output,'w')

        output.write(self.format())
        output.close()

    def format(self):
        return "\n".join((self._header, self._hosts))

    def header(self):
        params = {
            #'domain': self.find('domain').text,
            'listen': self.find('ip').attrib['address'],
            'range': ','.join(self.find('ip/dhcp/range').values()),
        }

        tmpl = """
strict-order
bind-interfaces
listen-address=%(listen)s
except-interface=lo
dhcp-range=%(range)s
"""
        return tmpl % headers

    def hosts(self):
        fmt = "dhcp-host=%(mac)s,%(ip)s,%(name)s"
        return "\n".join([fmt % h.attrib for h in self.find('ip/dhcp/range')])


LIBVIRT_BACKEND = 1
DNSMASQ_BACKEND = 2


def option_parser():
    parser = optparse.OptionParser("%prog [OPTION ...] NETWORK_XML")
    parser.add_option('-f', '--format', default=DNSMASQ_BACKEND, help='output format [dnsmasq]')
    parser.add_option('-o', '--output', default=False, help='output file')
    parser.add_option('-v', '--verbose', action="store_true",
        default=False, help='verbose mode')
    parser.add_option('-q', '--quiet', action="store_true",
        default=False, help='quiet mode')

    return parser


def main():
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

    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    network_xml = args[0]

    if options.format == DNSMASQ_BACKEND:
        fmtr = DnsmasqConfFmtr(network_xml)
        fmtr.dump(options.output)
    else:
        pass



if __name__ == '__main__':
    main()

# vim:sw=4:ts=4:et:ft=python:

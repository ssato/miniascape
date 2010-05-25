#
# Libvirt related stuff
#
# Copyright (C) 2009, 2010 Satoru SATOH <satoru.satoh at gmail.com>
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
# @see http://libvirt.org/formatdomain.html
# @see http://libvirt.org/html/libvirt-libvirt.html
#

import libvirt

try:
    import xml.etree.ElementTree as ET  # python >= 2.5
except ImportError:
    import elementtree.ElementTree as ET  # python <= 2.4; needs ElementTree.

import miniascape.config
import miniascape.qemu

from miniascape.globals import PKG_CONFIG_PATH
from miniascape.utils import runcmd



def svc_libvirtd(pkg_config_path=PKG_CONFIG_PATH):
    c = miniascape.config.init(pkg_config_path)

    return c.commands.svc_libvirtd


def is_libvirtd_running(svc_libvirtd):
    """Is the service "libvirtd" running?

    @return  Bool  True (running) or False (not)
    """
    (stat, _out) = runcmd("%s status 2>&1 > /dev/null" % svc_libvirtd)

    return (stat == 0)



class DomainXML(object):
    """Libvirt Domain XML object.
    """

    def __init__(self, name=False, path=False, pkg_config_path=PKG_CONFIG_PATH):
        """
        @name  Domain name
        @path  Filepath of domain XML
        """
        if not (name or path):
            raise RuntimeError("Neither domain name or file path was given.")

        self.config_path = pkg_config_path
        self.config = miniascape.config.init(pkg_config_path)

        if name:
            self.name = name

            if is_libvirtd_running(svc_libvirtd(self.config_path)):
                conn = connect()
                try:
                    dom = conn.lookupByName(name)
                    self.xml = dom.XMLDesc(0)
                    self.status = dom.info()[0]

                except libvirt.libvirtError:
                    raise RuntimeError(" Domain not found: '%s'" % name)
            else:
                self.xml = open("/etc/libvirt/qemu/%s.xml" % name).read()

        elif path:
            self.xml = open(path).read()

        self.parse(self.xml)

    def parse(self, xmlstr):
        """Parse domain xml string and returns {arch, [image path], ...}
        """
        qi = miniascape.qemu.qemu_img(self.config_path)

        tree = ET.fromstring(xmlstr)

        if not self.name:
            name = tree.findtext('name')

        self.arch = tree.find('os/type').attrib.get('arch')
        self.images = [e.attrib.get('file') for e in tree.findall('devices/disk/source')]

        self.base_images = [bp for bp in [base_image_path(p, qi) for p in images] if bp != '']


    def is_running(self):
        return self.status == libvirt.VIR_DOMAIN_RUNNING

    def is_shutoff(self):
        return self.status == libvirt.VIR_DOMAIN_SHUTOFF


# vim:sw=4:ts=4:et:

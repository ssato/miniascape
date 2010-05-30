#
# Virtualization related stuff
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
import re

import miniascape as m
from miniascape.globals import PKG_CONFIG_PATH

try:
    import xml.etree.ElementTree as ET  # python >= 2.5
except ImportError:
    import elementtree.ElementTree as ET  # python <= 2.4; needs ElementTree.



def svc_libvirtd(pkg_config_path=PKG_CONFIG_PATH):
    c = m.config.getInstance(pkg_config_path)

    return c.commands.svc_libvirtd


def is_libvirtd_running(pkg_config_path=PKG_CONFIG_PATH):
    """Is the service "libvirtd" running?

    @return  Bool  True (running) or False (not)
    """
    (stat, _out) = m.utils.runcmd("%s status 2>&1 > /dev/null" % svc_libvirtd(pkg_config_path))

    return (stat == 0)


def install_domain(domain_xml, pkg_config_path=PKG_CONFIG_PATH):
    """
    Install guest domain from its XML definition file.

    @domain_xml   Domain XML file path
    """
    if not is_libvirtd_running(pkg_config_path):
        return False

    conn = libvirt.open('qemu:///system')
    dom = conn.defineXML(domain_xml)

    return True


def base_image_path(image_path, pkg_config_path=PKG_CONFIG_PATH):
    """@return  the path of the base image of given image path or "" (given
    image not a delta image).

    example log:

    [root@foo ~]# qemu-img info /var/lib/libvirt/images/rhel-5-cluster-4-disk-1.qcow2
    image: /var/lib/libvirt/images/rhel-5-cluster-4-disk-1.qcow2
    file format: qcow2
    virtual size: 5.0G (5368709120 bytes)
    disk size: 32K
    cluster_size: 4096
    backing file: rhel-5-cluster-4-disk-1-base.qcow2 (actual path: /var/lib/libvirt/images/rhel-5-cluster-4-disk-1-base.qcow2)
    [root@foo ~]#
    """
    r = ""
    c = m.config.getInstance(pkg_config_path)

    (stat, out) = m.utils.runcmd("%s info %s" % (c.commands.qemu_img, image_path))
    if stat == 0:
        m = re.match(r'.*backing file: (?P<base>[^ ]+) \(actual path: (?P<base_full>[^ ]+)\)', out, re.DOTALL)
        if m:
            r = m.groupdict()['base_full']

    return r


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
        self.config = m.config.init(pkg_config_path)

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
                self.status = libvirt.VIR_DOMAIN_SHUTOFF

        elif path:
            self.xml = open(path).read()
            self.status = None

        self.parse(self.xml)

        if self.status is None:
            if is_libvirtd_running(svc_libvirtd(self.config_path)):
                conn = connect()
                try:
                    dom = conn.lookupByName(self.name)
                    self.status = dom.info()[0]

                except libvirt.libvirtError:
                    raise RuntimeError(" Domain not found: '%s'" % self.name)
            else:
                self.status = libvirt.VIR_DOMAIN_SHUTOFF

    def parse(self, xmlstr):
        """Parse domain xml string and returns {arch, [image path], ...}
        """
        tree = ET.fromstring(xmlstr)

        if not self.name:
            self.name = tree.findtext('name')

        self.arch = tree.find('os/type').attrib.get('arch')
        self.images = [e.attrib.get('file') for e in tree.findall('devices/disk/source')]

        self.base_images = [bp for bp in [base_image_path(p) for p in images] if bp != '']


    def is_running(self):
        return self.status == libvirt.VIR_DOMAIN_RUNNING

    def is_shutoff(self):
        return self.status == libvirt.VIR_DOMAIN_SHUTOFF


# vim:sw=4:ts=4:et:

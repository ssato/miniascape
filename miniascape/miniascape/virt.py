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
import logging
import os
import re

import miniascape as m
from miniascape.globals import PKG_CONFIG_PATH



class LibvirtNetwork(object):
    """Libvirt networks
    """

    def __init__(self, name, pkg_config_path=PKG_CONFIG_PATH):
        self.config_path = pkg_config_path
        self.config = m.config.getInstance(pkg_config_path)

        self.name = name
        self.xml = os.path.join(self.config.vmm.vnetxmldir, '%s.xml' % name)



class LibvirtDomain(object):
    """Libvirt (guest) domain.
    """

    def __init__(self, name="", xml_path="", pkg_config_path=PKG_CONFIG_PATH):
        """
        @name       Domain name. name or xml_path must be set (not empty).
        @xml_path   Domain XML's path (absolute)
        @pkg_config_path  Common config file path
        """
        self.config_path = pkg_config_path
        self.config = m.config.getInstance(pkg_config_path)

        self.connection = False

        if xml_path:
            self.xml_path = xml_path
            name = m.utils.xpath_eval('/domain/name', xml_path)

            assert name 
        else:
            assert name 

            self.name = name

            # TODO: Get domain XML content from libvirtd.
            #if self.is_libvirtd_running():
            #    ...
            self.xml_path = os.path.join(self.config.vmm.vmxmldir, "%s.xml" % self.name)

    def vmm_connect(self):
        if not self.connection:
            try:
                conn = libvirt.open(self.config.vmm.connect)
                self.connection = conn
            except libvirt.libvirtError, m:
                logging.info(" errmsg='%s'" % m)
                raise RuntimeError(" Could not connect to vmm")
            
    def is_libvirtd_running(self):
        """Is the service "libvirtd" running?

        @return  Bool  True (running) or False (not)
        """
        (stat, _out) = m.utils.runcmd("%s status 2>&1 > /dev/null" % self.config.commands.svc_libvirtd)
        return (stat == 0)

    def xml(self):
        if self.xml_path:
            return open(self.xml_path).read()

    def parse(self):
        """Parse domain xml and store various guest profile data.
        """
        self.arch = m.utils.xpath_eval('/domain/os/type/@arch', self.xml_path)
        self.images = m.utils.xpath_eval('/domain/devices/disk[@type="file"]/source/@file', self.xml_path)
        self.networks = m.utils.unique(
            m.utils.xpath_eval('/domain/devices/interface[@type="network"]/source/@network', self.xml_path)
        )

        self.base_images = m.utils.unique(
            (bp for bp in [self.base_image_path(p) for p in self.images] if bp)
        )

    def status(self):
        if self.is_libvirtd_running():
            self.vmm_connect()
            dom = self.connection.lookupByName(self.name)
            return dom.info()[0]
        else:
            return libvirt.VIR_DOMAIN_SHUTOFF

    def is_running(self):
        return self.status() == libvirt.VIR_DOMAIN_RUNNING

    def is_shutoff(self):
        return self.status() == libvirt.VIR_DOMAIN_SHUTOFF

    def install(self):
        """Install this domain.
        """
        if self.is_libvirtd_running():
            self.vmm_connect()
            dom = self.connection.defineXML(self.xml_path)
        else:
            logging.error(" libvirtd service is not running. Start libvirtd and retry installation.")


    def uninstall(self):
        """Uninstall this guest domain.
        """
        if self.is_libvirtd_running():
            if self.status() == libvirt.VIR_DOMAIN_SHUTOFF:
                self.vmm_connect()
                dom = self.connection.lookupByName(self.name)
                dom.undefine()
            else:
                logging.info(" Domain %s is not shutoff." % domain_name)

    def base_image_path(self, image_path):
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

        (stat, _out) = m.utils.runcmd("%s info %s" % (self.config.commands.qemu_img, image_path))
        if stat == 0:
            m = re.match(r'.*backing file: (?P<base>[^ ]+) \(actual path: (?P<base_full>[^ ]+)\)', _out, re.DOTALL)
            if m:
                r = m.groupdict()['base_full']

        return r


# vim:sw=4:ts=4:et:

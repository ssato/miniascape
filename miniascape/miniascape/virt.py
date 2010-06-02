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
import re

import miniascape as m
from miniascape.globals import PKG_CONFIG_PATH



def svc_libvirtd(pkg_config_path=PKG_CONFIG_PATH):

    return c.commands.svc_libvirtd


def is_libvirtd_running(pkg_config_path=PKG_CONFIG_PATH):
    """Is the service "libvirtd" running?

    @return  Bool  True (running) or False (not)
    """
    c = m.config.getInstance(pkg_config_path)
    (stat, _out) = m.utils.runcmd("%s status 2>&1 > /dev/null" % c.commands.svc_libvirtd)

    return (stat == 0)


def install_domain(domain_xml, pkg_config_path=PKG_CONFIG_PATH):
    """
    Install guest domain from its XML definition file.

    @domain_xml   Domain XML file path
    """
    c = m.config.getInstance(pkg_config_path)

    if is_libvirtd_running(pkg_config_path):
        try:
            conn = libvirt.open('qemu:///system')
            dom = conn.defineXML(domain_xml)
            return True

        except libvirt.libvirtError, m:
            logging.info(" errmsg='%s'" % m)
            return False
    else:
        logging.info(" libvirtd service is not running.")
        return False


def uninstall_domain(domain_name, pkg_config_path=PKG_CONFIG_PATH):
    """
    Uninstall guest domain from its XML definition file.

    @domain_name  Guest domain name
    """
    c = m.config.getInstance(pkg_config_path)

    if is_libvirtd_running(pkg_config_path):
        try:
            conn = libvirt.open('qemu:///system')
            dom = conn.lookupByName(domain_name)
            status = dom.info()[0]
        
            if status == libvirt.VIR_DOMAIN_SHUTOFF:
                dom.undefine()
                return True
            else:
                logging.info(" Domain %s is not shutoff." % domain_name)
                return False

        except libvirt.libvirtError, m:
            logging.info(" errmsg='%s'" % m)
            return False
    else:
        logging.info(" libvirtd service is not running.")
        return False


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

    def __init__(self, path, name="", pkg_config_path=PKG_CONFIG_PATH):
        """
        @path  Domain XML path
        @pkg_config_path  Common config file path
        """
        self.name = name

        self.config_path = pkg_config_path
        self.config = m.config.getInstance(pkg_config_path)

        self.path = self.source = path
        self.xml = open(path).read()

        self.__parse(path)

    def __parse(self, xmlfile):
        """Parse domain xml string and returns {arch, [image path], ...}
        """
        if not self.name:
            self.name = xpath_eval('/domain/name', xmlfile)

        self.arch = xpath_eval('/domain/os/type/@arch')
        self.images = xpath_eval('/domain/devices/disk[@type="file"]/source/@file')
        self.networks = m.utils.unique(xpath_eval('/domain/devices/interface[@type="network"]/source/@network'))

        self.base_images = m.utils.unique((bp for bp in [base_image_path(p) for p in self.images] if bp))


    def is_running(self):
        return self.status == libvirt.VIR_DOMAIN_RUNNING

    def is_shutoff(self):
        return self.status == libvirt.VIR_DOMAIN_SHUTOFF


# vim:sw=4:ts=4:et:

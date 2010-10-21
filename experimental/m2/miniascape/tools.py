#
# Wrapper for external tools
#
# Copyright (C) 2010 Satoru SATOH <satoru.satoh at gmail.com>
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

import os
import re

import miniascape.utils as U
from miniascape.globals import QEMU_IMG, VIRT_INSTALL, SERVICE_LIBVIRTD



def is_libvirtd_running():
    """Is the service "libvirtd" running?

    @return  Bool  True (running) or False (not)
    """
    (rc, _out) = U.runcmd("%s status 2>&1 > /dev/null 2>/dev/null" % SERVICE_LIBVIRTD)
    return (rc == 0)


def create_delta_image(base_image_path, delta_image_name):
    """
    @base_image_path    Base image's path (absolute / relative)
    @delta_image_name   Delta image's name (basename)
    """
    assert base_image_path_for_delta_image_path(base_image_path) == "", "Image %s is not a base image" % base_image_path

    (bdir, bn) = (os.path.dirname(base_image_path), os.path.basename(base_image_path))
    assert bn != delta_image_name, "base and delta images are same name!: %s" % bn

    (rc, out) = U.runcmd("cd %s && %s create -f qcow2 -b %s %s" % (bdir, QEMU_IMG, bn, delta_image_name))
    if rc != 0:
        raise RuntimeError(" create_delta_image: error while creating the delta image %s for %s" % (delta_image_name, bn))


def base_image_path_for_delta_image_path(image_path):
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

    (rc, out) = U.runcmd("%s info %s" % (QEMU_IMG, image_path))
    if rc != 0:
        raise RuntimeError(" base_image_path: error while getting the base image path of %s" % image_path)

    matched = re.match(r'.*backing file: (?P<base>[^ ]+) \(actual path: (?P<base_full>[^ ]+)\)', out, re.DOTALL)
    if matched:
        r = matched.groupdict()['base_full']

    return r


# vim:sw=4:ts=4:et:

#
# Qemu related stuff
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

import re
import sys

import miniascape.config

from miniascape.globals import PKG_CONFIG_PATH
from miniascape.utils import runcmd



def qemu_img(config_path):
    """Get the path to qemu-img from config file.

    @see miniascape.config
    """
    c = miniascape.config.init(config_path)
    return c.commands.qemu_img


def base_image_path(image_path, config_path=PKG_CONFIG_PATH):
    """Get the path of the base image of given image path.  "" will return if
    given image is not a delta image.


    Here is an example of qemu-img's output:

    [root@foo ~]# qemu-img info /var/lib/libvirt/images/rhel-5-cluster-4-disk-1.qcow2
    image: /var/lib/libvirt/images/rhel-5-cluster-4-disk-1.qcow2
    file format: qcow2
    virtual size: 5.0G (5368709120 bytes)
    disk size: 32K
    cluster_size: 4096
    backing file: rhel-5-cluster-4-disk-1-base.qcow2 (actual path: /var/lib/libvirt/images/rhel-5-cluster-4-disk-1-base.qcow2)
    [root@foo ~]#
    """
    ret = ""
    qi = qemu_img(config_path)

    (stat, out) = runcmd("%s info %s" % (qi, image_path))

    if stat == 0:
        m = re.match(r'.*backing file: (?P<base>[^ ]+) \(actual path: (?P<base_full>[^ ]+)\)', out, re.DOTALL)
        if m:
            ret = m.groupdict()['base_full']
            assert ret != ""

    return ret


# vim:sw=4:ts=4:et:

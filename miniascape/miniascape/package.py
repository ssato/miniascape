#
# * repackage virtualization guest domain from definition file
# * build and package virtualization guest domain
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
# @see http://www.qemu.org/qemu-doc.html#SEC19
#

import commands
import libvirt
import logging
import os
import re
import shutil
import sys


"""
$domain.xml
$domain.images
#if $getVar('variant', '')
$domain.name
$variant
$timestamp
"""



def do_repackage_setup(domain_xml, builddir):
    """setup packaging dir and files to re-package vm images.

    @domain_xml  Domain XML file path
    @builddir    
    """
    if domain_xml:
        domxml_content = open(domain_xml).read()
    else:
        domxml_content = get_domain_xml(domain_name)

    domain_images = domain_image_paths(domxml_content)

    substs = {
        '%%DOMAIN_NAME%%': domain_name,
        '%%DOMAIN_VARIANT%%': domain_variant,
        '%%DOMAIN_IMAGES%%': ' '.join((os.path.basename(p) for p in domain_images))
    }

    createdir(builddir)
    createdir(os.path.join(builddir, M4DIR))

    open("%s/%s.xml" % (builddir, domain_name), 'w').write(domxml_content)

    copyfile(os.path.join(libpath, AUXDIR, 'rpm.mk'), os.path.join(builddir, AUXDIR))
    copyfile(os.path.join(libpath, M4DIR, 'qemu.m4'), os.path.join(builddir, M4DIR))
    copyfile(os.path.join(libpath, M4DIR, 'rpm.m4'), os.path.join(builddir, M4DIR))
    copyfile(os.path.join(libpath, 'repackage', 'Makefile.am.in'), os.path.join(builddir, 'Makefile.am'))
    copyfile(os.path.join(libpath, 'repackage', 'README.in'), builddir)
    copyfile(os.path.join(libpath, 'repackage', 'vm-image.spec.in'), \
        os.path.join(builddir, 'vm-%s-%s.spec.in' % (domain_name, domain_variant)))

    substfile(os.path.join(libpath, 'repackage', 'configure.ac.in'), os.path.join(builddir, 'configure.ac'), substs)

    for image in domain_images:
        copyfile(image, builddir)


def do_package_setup(libpath, domain_name, domain_variant, builddir, *args):
    """setup packaging dir and files to package vm images.
    """
    substs = {
        '%%DOMAIN_NAME%%': domain_name,
        '%%DOMAIN_VARIANT%%': domain_variant,
    }

    createdir(builddir)
    createdir(os.path.join(builddir, 'data'))
    createdir(os.path.join(builddir, M4DIR))

    # configure.ac.in  data  vm-image.spec.in
    copyfile(os.path.join(libpath, AUXDIR, 'rpm.mk'), os.path.join(builddir, AUXDIR))
    copyfile(os.path.join(libpath, M4DIR, 'libvirt.m4'), os.path.join(builddir, M4DIR))
    copyfile(os.path.join(libpath, M4DIR, 'qemu.m4'), os.path.join(builddir, M4DIR))
    copyfile(os.path.join(libpath, M4DIR, 'rpm.m4'), os.path.join(builddir, M4DIR))
    copyfile(os.path.join(libpath, M4DIR, 'virtinst.m4'), os.path.join(builddir, M4DIR))
    copyfile(os.path.join(libpath, 'package', 'Makefile.am.in'), os.path.join(builddir, 'Makefile.am'))
    copyfile(os.path.join(libpath, 'package', 'README.in'), builddir)
    copyfile(os.path.join(libpath, 'package', 'vm-image.spec.in'), \
        os.path.join(builddir, 'vm-%s-%s.spec.in' % (domain_name, domain_variant)))
    copyfile(os.path.join(libpath, 'package', 'data', 'Makefile.am.in'), os.path.join(builddir, 'data', 'Makefile.am'))

    substfile(os.path.join(libpath, 'package', 'configure.ac.in'), os.path.join(builddir, 'configure.ac'), substs)


# vim:sw=4:ts=4:et:

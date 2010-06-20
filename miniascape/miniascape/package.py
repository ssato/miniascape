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

import logging
import os
import re

import miniascape as m
from miniascape.globals import PKG_CONFIG_PATH



class Workflow(object):

    def __init__(self, name, variant="", topdir="", pkg_config_path=PKG_CONFIG_PATH):
        """
        @name         VM's name.
        @pkg_config_path  Common config file path
        """
        self.config_path = pkg_config_path
        self.config = m.config.getInstance(pkg_config_path)

        self.name = name

        if variant:
            self.variant = variant
        else:
            self.variant = self.config.pack.variant

        self.package_name = "vm-%s-%s" % (self.name, self.variant)
        self.package_version = self.config.pack.version

        if topdir:
            self.workdir = os.path.join(prefix, "%s-%s" % (self.package_name, self.package_version))
        else:
            self.workdir = "./%s-%s" % (self.package_name, self.package_version)

    def setup_workdir(self, *args, **kwargs):
        """
        @throw OSError, etc.
        """
        os.makedirs(self.workdir, 0700)

    def setup_buildfiles(self, *args, **kwargs):
        pass

    def setup_data(self, *args, **kwargs):
        pass

    def setup(self, *args, **kwargs):
        self.setup_workdir(*args, **kwargs)
        self.setup_data(*args, **kwargs)
        self.setup_buildfiles(*args, **kwargs)

    def build_main(self, *args, **kwargs):
        pass

    def build_archive(self, *args, **kwargs):
        pass

    def build_src_rpm(self, *args, **kwargs):
        pass

    def build_bin_rpm(self, *args, **kwargs):
        pass

    def build(self, *args, **kwargs):
        self.build_main(*args, **kwargs)
        self.build_archive(*args, **kwargs)
        self.build_src_rpm(*args, **kwargs)

    def template_output(self, tmpl):
        return os.path.join(self.workdir, tmpl.replace('.tmpl',''))



class RepackWorkflow(Workflow):

    def setup_buildfiles(self, *args, **kwargs):
        tmpls = ['Makefile.am.tmpl', 'README.tmpl', 'configure.ac.tmpl',  'vm.spec.in.tmpl']
        tmpls = [os.path.join(self.config.dirs.templatesdir, "repack", t) for t in tmpls]

        for t in tmpls:
            m.utils.compile_template(t, self.template_output(t), self.domain)

        os.makedirs(os.path.join(self.workdir, 'aux'))
        os.makedirs(os.path.join(self.workdir, 'aux', 'm4'))

        m.utils.copyfile(os.path.join(self.config.dirs.auxdir, 'rpm.mk'), self.workdir, force=True)

        for mf in ('libvirt.m4', 'package.m4', 'python.m4', 'qemu.m4', 'rpm.m4'):
            m.utils.copyfile(os.path.join(self.config.dirs.m4dir, mf), self.workdir, force=True)

    def setup_data(self, *args, **kwargs):
        self.domain = m.virt.LibvirtDomain(self.name, self.config_path)

        self.domain.parse()

        xml = re.sub(r'<uuid>.+</uuid>\n', '', str(self.domain))
        open(os.path.join(self.workdir, "%s.xml" % self.name), "w").write(xml)

        for img in self.images + self.base_images:
            m.utils.copyfile(img, os.path.join(self.workdir, os.path.basename(img)))




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

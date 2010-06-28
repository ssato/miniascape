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

import logging
import os
import re

import miniascape.config as C
import miniascape.tools as T
import miniascape.utils as U
import miniascape.virt as V

from miniascape.globals import PKG_CONFIG_PATH



class PackageDTO(C.ODict):

    def __init__(self, name, variant, version):
        super(self.__class__, self).__init__()

        self.domain_name = name
        self.variant = variant

        self.name = "vm-%s-%s" % (self.domain_name, self.variant)
        self.version = version
        self.virtual_name = "vm-%s" % self.domain_name

        self.provides = self.virtual_name



class DomainDTO(C.ODict):

    def __init__(self, name, xml_path, xml_store_path, base_images=[], delta_images=[]):
        """
        @base_images   Base image path list (absolute path)
        @delta_images  Delta image path list (absolute path)
        """
        super(self.__class__, self).__init__()

        self.name = name
        self.xml_path = xml_path
        self.xml_store_path = xml_store_path

        self.base_images = []
        self.delta_images = []

        if base_images:
            self.add_base_images(base_images)

        if delta_images:
            self.add_delta_images(delta_images)

    def add_base_images(self, path_list=[]):
        for path in path_list:
            i = C.ODict()
            i['dir'] = os.path.dirname(path)
            i['name'] = os.path.basename(path)
            self.base_images.append(i)

    def add_delta_images(self, path_list=[]):
        for path in path_list:
            i = C.ODict()
            i['dir'] = os.path.dirname(path)
            i['name'] = os.path.basename(path)
            self.delta_images.append(i)



class BuildProcess(C.ODict):

    # inherited class must define the followings!
    templates_subdir = 'DUMMY'
    templates = []
    m4files = []

    def __init__(self, name, variant="", version="", topdir=os.curdir, pkg_config_path=PKG_CONFIG_PATH):
        """
        @name         VM's name.
        @pkg_config_path  Common config file path
        """
        self.config_path = pkg_config_path
        self.config = C.getInstance(pkg_config_path)

        if not variant:
            variant = self.config.pack.variant

        if not version:
            version = self.config.pack.version

        self.domain = DomainDTO(name, self.config.vmm.vmxmldir, self.config.vmm.vmxmlstoredir)
        self.package = PackageDTO(name, variant, version)

        self.workdir = os.path.join(topdir, "%s-%s" % (self.package.name, self.package.version))

    def setup(self, prebuild=True):
        logging.info(" setup starts...")
        self.setup_workdir()
        self.setup_data()
        self.setup_buildfiles()
        logging.info(" ...setup ends")

    def prebuild(self):
        logging.info(" prebuild starts...")
        self.runcmd("cd %s && autoreconf -vfi" % self.workdir)
        logging.info(" ...prebuild ends")

    def build(self, *args, **kwargs):
        logging.info(" build starts...")
        self.build_main(*args, **kwargs)
        self.postbuild(*args, **kwargs)
        logging.info(" ...build ends")

    def pack(self, binary=False):
        logging.info(" pack starts...")
        self.prebuild()
        self.make_archive()
        self.pack_src()

        if binary:
            self.pack_bin()

        logging.info(" ...pack ends")

    def setup_workdir(self):
        """@throw OSError, etc.
        """
        os.makedirs(self.workdir, 0700)

    def setup_buildfiles(self):
        tmpldir = os.path.join(self.config.dirs.templatesdir, self.templates_subdir)

        for t in (os.path.join(tmpldir, t) for t in self.templates):
            U.compile_template(t, self.template_output(t), self)

        U.copyfile(os.path.join(self.config.dirs.auxdir, 'rpm.mk'), self.workdir, force=True)

        m4dir = os.path.join(self.workdir, 'm4')
        os.makedirs(m4dir)
        for mf in self.m4files:
            U.copyfile(os.path.join(self.config.dirs.m4dir, mf), m4dir, force=True)

    def setup_data(self):
        pass

    def build_main(self, *args, **kwargs):
        self.runcmd("cd %s && make" % self.workdir)

    def postbuild(self, *args, **kwargs):
        pass

    def make_archive(self):
        self.runcmd("cd %s && make dist" % self.workdir)

    def pack_src(self):
        self.runcmd("cd %s && make srpm" % self.workdir)

    def pack_bin(self):
        #self.runcmd("cd %s && mock -r %s *.src.rpm" % (self.workdir, self.config.pack.target_dist))
        self.runcmd("cd %s && make rpm" % self.workdir)

    def template_output(self, tmpl):
        return os.path.join(self.workdir, tmpl.replace('.tmpl',''))

    def runcmd(self, cmds):
        (rc, out) = U.runcmd(cmds)
        if rc !=0:
            raise RuntimeError(" rc=%d, err='%s'" % (rc, out))



class RepackProcess(BuildProcess):

    templates_subdir = 'repack'

    templates = [
        'Makefile.am.tmpl',
        'README.tmpl',
        'README.base.tmpl',
        'configure.ac.tmpl',
        'vm.spec.in.tmpl',
    ]

    m4files = [
        'miniascape.m4',
        'package.m4',
        'rpm.m4',
    ]

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        domain = V.LibvirtDomain(self.domain.name, pkg_config_path=self.config_path)
        domain.parse()

        self._libvirtDomain = domain

    def setup_data(self, *args, **kwargs):
        xml = re.sub(r'<uuid>.+</uuid>\n', '', str(self._libvirtDomain))
        open(os.path.join(self.workdir, "%s.xml" % self.domain.name), "w").write(xml)

        base_images = []
        delta_images = []

        for dp in self._libvirtDomain.images:
            delta_images.append(dp)

            bp = T.base_image_path_for_delta_image_path(dp)

            if bp:
                base_images.append(bp)

                U.copyfile(dp, os.path.join(self.workdir, os.path.basename(dp)))
                U.copyfile(bp, os.path.join(self.workdir, os.path.basename(bp)))
            else:
                (bpn0,bpext) = os.path.splitext(dp)
                bp = bpn0 + "-base" + bpext
                base_images.append(bp)

                bp1 = os.path.join(self.workdir, os.path.basename(bp))  # base_image_path (dst)

                U.copyfile(dp, bp1)
                T.create_delta_image(bp1, os.path.basename(dp))



class PackProcess(BuildProcess):

    def setup_buildfiles(self, *args, **kwargs):
        tmpls = ['Makefile.am.tmpl', 'README.tmpl', 'configure.ac.tmpl',  'vm.spec.in.tmpl']
        tmpls = [os.path.join(self.config.dirs.templatesdir, "pack", t) for t in tmpls]

        for t in tmpls:
            U.compile_template(t, self.template_output(t), self.domain)

        os.makedirs(os.path.join(self.workdir, 'aux'))
        os.makedirs(os.path.join(self.workdir, 'aux', 'm4'))

        U.copyfile(os.path.join(self.config.dirs.auxdir, 'rpm.mk'), self.workdir, force=True)

        for mf in ('libvirt.m4', 'package.m4', 'python.m4', 'qemu.m5', 'rpm.m4', 'virtinst.m4'):
            U.copyfile(os.path.join(self.config.dirs.m4dir, mf), self.workdir, force=True)




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

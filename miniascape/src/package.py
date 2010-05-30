#! /usr/bin/python
#
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

import errno
import logging
import optparse
import os
import sys

import miniascape as m
import miniascape.config

from miniascape.globals import PKG_CONFIG_PATH, PKG_SYSCONFDIR, PKG_DATADIR

import libvirt
import re



DOMAIN_VARIANT = 'minimal'

RPMNAME_PREFIX = 'vm'
RPMNAME_SUFFIX = DOMAIN_VARIANT

AUXDIR = 'aux'
M4DIR = os.path.join(AUXDIR, 'm4')



def connect():
    #return libvirt.openReadOnly(None)
    return libvirt.openReadOnly('qemu:///system')


def package_name(domain_name, prefix=RPMNAME_PREFIX, suffix=RPMNAME_SUFFIX):
    return '%s-%s-%s' % (prefix, domain_name, suffix)


def make_builddir(workdir, domain_name):
    return os.path.join(workdir, package_name(domain_name))


# actions:
def do_repackage_setup(libpath, domain_name, domain_variant, domain_xml, builddir, *args):
    """setup packaging dir and files to re-package vm images.
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

    m.utils.mkdir(builddir)
    m.utils.mkdir(os.path.join(builddir, M4DIR))

    open("%s/%s.xml" % (builddir, domain_name), 'w').write(domxml_content)

    m.utils.copyfile(os.path.join(libpath, AUXDIR, 'rpm.mk'), os.path.join(builddir, AUXDIR))
    m.utils.copyfile(os.path.join(libpath, M4DIR, 'qemu.m4'), os.path.join(builddir, M4DIR))
    m.utils.copyfile(os.path.join(libpath, M4DIR, 'rpm.m4'), os.path.join(builddir, M4DIR))
    m.utils.copyfile(os.path.join(libpath, 'repackage', 'Makefile.am.in'), os.path.join(builddir, 'Makefile.am'))
    m.utils.copyfile(os.path.join(libpath, 'repackage', 'README.in'), builddir)
    m.utils.copyfile(os.path.join(libpath, 'repackage', 'vm-image.spec.in'), \
        os.path.join(builddir, 'vm-%s-%s.spec.in' % (domain_name, domain_variant)))

    m.utils.substfile(os.path.join(libpath, 'repackage', 'configure.ac.in'), os.path.join(builddir, 'configure.ac'), substs)

    for image in domain_images:
        m.utils.copyfile(image, builddir)


def do_package_setup(libpath, domain_name, domain_variant, builddir, *args):
    """setup packaging dir and files to package vm images.
    """
    substs = {
        '%%DOMAIN_NAME%%': domain_name,
        '%%DOMAIN_VARIANT%%': domain_variant,
    }

    m.utils.mkdir(builddir)
    m.utils.mkdir(os.path.join(builddir, 'data'))
    m.utils.mkdir(os.path.join(builddir, M4DIR))

    # configure.ac.in  data  vm-image.spec.in
    m.utils.copyfile(os.path.join(libpath, AUXDIR, 'rpm.mk'), os.path.join(builddir, AUXDIR))
    m.utils.copyfile(os.path.join(libpath, M4DIR, 'libvirt.m4'), os.path.join(builddir, M4DIR))
    m.utils.copyfile(os.path.join(libpath, M4DIR, 'qemu.m4'), os.path.join(builddir, M4DIR))
    m.utils.copyfile(os.path.join(libpath, M4DIR, 'rpm.m4'), os.path.join(builddir, M4DIR))
    m.utils.copyfile(os.path.join(libpath, M4DIR, 'virtinst.m4'), os.path.join(builddir, M4DIR))
    m.utils.copyfile(os.path.join(libpath, 'package', 'Makefile.am.in'), os.path.join(builddir, 'Makefile.am'))
    m.utils.copyfile(os.path.join(libpath, 'package', 'README.in'), builddir)
    m.utils.copyfile(os.path.join(libpath, 'package', 'vm-image.spec.in'), \
        os.path.join(builddir, 'vm-%s-%s.spec.in' % (domain_name, domain_variant)))
    m.utils.copyfile(os.path.join(libpath, 'package', 'data', 'Makefile.am.in'), os.path.join(builddir, 'data', 'Makefile.am'))

    m.utils.substfile(os.path.join(libpath, 'package', 'configure.ac.in'), os.path.join(builddir, 'configure.ac'), substs)


def do_build(domain_name, builddir):
    """Build domain $domain_name.
    """
    if not os.path.isdir(builddir):
        raise RuntimeError("build dir is not ready! 'setup' it first.")

    (stat, out) = runcmd("cd %s && autoreconf -vfi && ./configure && make" % builddir)
    if stat != 0:
        raise RuntimeError("Build stopped during 'make': '%s'" % out)

    return stat


def do_dist(domain_name, builddir):
    """Build dist.
    """
    if not os.path.isdir(builddir):
        raise RuntimeError("build dir is not ready! 'setup' it first.")

    (stat, out) = runcmd("cd %s && (test -f configure || autoreconf -vfi) && ./configure && make dist-@SOURCE_ZIP@" % builddir)
    if stat != 0:
        raise RuntimeError("Build stopped during 'make dist': '%s'" % out)

    return stat


def do_package(domain_name, builddir):
    """Build [s]rpm of $domain_name
    """
    if not os.path.isdir(builddir):
        raise RuntimeError("build dir is not ready! 'setup' and 'build' it first.")

    (stat, out) = runcmd("cd %s && make srpm && make rpm" % builddir)
    if stat != 0:
        raise RuntimeError("Build stopped during 'make [s]rpm': '%s'" % out)

    return stat


def option_parser():
    parser = optparse.OptionParser("""%prog COMMAND [OPTION ...] [ARGS ...]
Commands: pack[age] and repack[age]

Examples:
    %prog pack dom-1 
    %prog repack dom-1.xml 
"""
    )
    parser.add_option('-L', '--libpath', default=PKG_DATADIR,
        help='Path to search library files [%default]')
    parser.add_option('', '--workdir', default=os.curdir, help='Working directory [%default]')
    parser.add_option('', '--variant', default=DOMAIN_VARIANT, help='Domain variant [%default]')
    parser.add_option('-v', '--verbose', dest='verbose', action="store_true",
        default=False, help='verbose mode')
    parser.add_option('-q', '--quiet', dest='quiet', action="store_true",
        default=False, help='quiet mode')

    sog = optparse.OptionGroup(parser, "Staging options")
    sog.add_option('', '--build', action="store_true", default=False,
        help='Setup and build (domain installation). Not effective for "repackage" command.')
    sog.add_option('', '--package', action="store_true", default=False, help='Setup, build and package')
    parser.add_option_group(sog)

    #rog = optparse.OptionGroup(parser, "Options for 'repackage'")
    #rog.add_option('', '--xml', default=False, help='Domain XML in full path.')
    #parser.add_option_group(rog)

    return parser


def main(argv=sys.argv):
    loglevel = logging.INFO

    parser = option_parser()

    if len(argv) < 2:
        parser.print_usage()
        sys.exit(1)

    cmd = argv[1]

    if cmd.startswith('pack'):
        cmd = 'package'
    elif cmd.startswith('repack'):
        cmd = 'repackage'

    (options, args) = parser.parse_args(argv[2:])

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

    if cmd == 'package':
        if len(args) < 1:
            print >> sys.stderr, "%s pack[age] DOMAIN_NAME [OPTIONS...]" % sys.argv[0]
            sys.exit(1)

        domain_name = args[0]
        builddir = make_builddir(options.workdir, domain_name)

        do_package_setup(options.libpath, domain_name, options.variant, builddir)

    elif cmd == 'repackage':
        if len(args) < 1:
            print >> sys.stderr, "%s repack[age] DOMAIN_XML [OPTIONS...]" % sys.argv[0]
            sys.exit(1)

        domain_xml = args[0]
        domain_name = domainname_from_xml(domain_xml)
        builddir = make_builddir(options.workdir, domain_name)

        stat = domain_status(domain_name)
        if stat != libvirt.VIR_DOMAIN_SHUTOFF:
            if stat == libvirt.VIR_DOMAIN_RUNNING:
                logging.error(" VM '%s' is still running. Please shutdown it first." % domain_name)
            else:
                logging.error(" VM '%s' is unknown state." % domain_name)

            sys.exit(1)

        do_repackage_setup(options.libpath, domain_name, options.variant, domain_xml, builddir)
    else:
        parser.print_usage()
        sys.exit(1)

    ret = 0
    if options.build or options.package:
        ret = do_build(domain_name, builddir)
        if ret != 0:
            raise RuntimeError("build failed.")

    ret = do_dist(domain_name, builddir)
    if ret != 0:
        raise RuntimeError("'make dist' failed.")

    if options.package:
        ret = do_package(domain_name, builddir)

    sys.exit(ret)


if __name__ == '__main__':
    main()

# vim:sw=4:ts=4:et:ft=python:

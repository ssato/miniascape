#! /usr/bin/python
#
# Configure libvirt networks and these DHCP settings
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
# @see http://pyyaml.org/wiki/PyYAMLDocumentation
# @see http://cheetahtemplate.org/learn.html
# @see http://libvirt.org/formatnetwork.html
# @see http://www.thekelleys.org.uk/dnsmasq/doc.html
# @see http://www.thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html
#

import Cheetah.Template
import errno
import optparse
import os
import sys
import yaml  # PyYAML


# FIXME: These should be dynamically configured at './configure' time.
CONF_DIR = '/etc/miniascape/networks'

NETXML_TMPL_DIR = '/usr/share/miniascape/templates/networks'
DNSMASQ_TMPL_DIR = os.path.join(NETXML_TMPL_DIR, 'dnsmasq')

NETXML_CONF_DIR = '/var/lib/miniascape/networks'
DNSMASQ_CONF_DIR = '/var/lib/miniascape/networks/dnsmasq'



def compile(template_path, params):
    tmpl = Cheetah.Template.Template(file=template_path, searchList=params)
    return tmpl.respond()


def load_config(config_path):
    return yaml.load(open(config_path, 'r'))


def main():
    parser = optparse.OptionParser("%prog [OPTION ...] NET_NAME")
    parser.add_option('', '--conf', help='parameter config file ')

    tog = optparse.OptionGroup(parser, "Template options")
    tog.add_option('', '--netxml-template', help='Libvirt network XML template file ')
    tog.add_option('', '--dnsmasq-conf-template', help='Dnsmasq config template ')
    tog.add_option('', '--dnsmasq-hostsfile-template', help='Dnsmasq hostsfile template ')
    parser.add_option_group(tog)

    oog = optparse.OptionGroup(parser, "Output options")
    oog.add_option('', '--netxml', help='Libvirt network XML template file ')
    oog.add_option('', '--dnsmasq-conf', help='Dnsmasq config template ')
    oog.add_option('', '--dnsmasq-hostsfile', help='Dnsmasq hostsfile template ')
    parser.add_option_group(oog)

    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        sys.exit(errno.EINVAL)

    netname = args[0]

    conf = os.path.join(CONF_DIR, 'net-1.yaml')

    netxml_tmpl = os.path.join(NETXML_TMPL_DIR, 'net-x.xml.tmpl')
    dnsmasq_conf_tmpl = os.path.join(DNSMASQ_TMPL_DIR, 'net-x.conf.tmpl')
    dnsmasq_hostsfile_tmpl = os.path.join(DNSMASQ_TMPL_DIR, 'net-x.hostsfile.tmpl')

    netxml = os.path.join(NETXML_CONF_DIR, '%s.xml' % netname)
    dnsmasq_conf = os.path.join(DNSMASQ_CONF_DIR, '%s.conf' % netname)
    dnsmasq_hostsfile = os.path.join(DNSMASQ_CONF_DIR, '%s.hostsfile' % netname)

    if options.conf:
        conf = options.conf

    if options.netxml_template:
        netxml_tmpl = options.netxml_template

    if options.dnsmasq_conf_template:
        dnsmasq_conf_tmpl = options.dnsmasq_conf_template

    if options.dnsmasq_hostsfile_template:
        dnsmasq_hostsfile_tmpl = options.dnsmasq_hostsfile_template

    if options.netxml:
        netxml = options.netxml

    if options.dnsmasq_conf:
        dnsmasq_conf = options.dnsmasq_conf

    if options.dnsmasq_hostsfile:
        dnsmasq_hostsfile = options.dnsmasq_hostsfile

    for f in (conf, netxml_tmpl, dnsmasq_conf_tmpl, dnsmasq_hostsfile_tmpl):
        if not os.path.exists(f):
            print >> sys.stderr, "Could not find '%s'" % f
            sys.exit(errno.EIO)

    conf_params = load_config(conf)

    netxml_content = compile(netxml_tmpl, conf_params)
    dnsmasq_conf_content = compile(dnsmasq_conf_tmpl, conf_params)
    dnsmasq_hostsfile_content = compile(dnsmasq_hostsfile_tmpl, conf_params)

    open(netxml, 'w').write(netxml_content)
    open(dnsmasq_conf, 'w').write(dnsmasq_conf_content)
    open(dnsmasq_hostsfile, 'w').write(dnsmasq_hostsfile_content)


if __name__ == '__main__':
    main()

# vim: set sw=4 ts=4 et:

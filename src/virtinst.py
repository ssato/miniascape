#! /usr/bin/python
#
# virt-install wrapper script
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

import Cheetah.Template
import commands
import errno
import optparse
import os
import sys
import yaml  # PyYAML



SITE_CONFIG = '/etc/miniascape/profiles/site.cfg'

TEMPLATE = r"""
$virtinst \
--hvm \
--accelerate \
--name=$name \
--connect=$connect \
--ram=$ram \
--arch=$arch \
--vcpus=$vcpus \
#if $getVar('cpuset', '')
--cpuset=$cpuset \
#end if
--keymap=$keymap \
--os-variant=$os_variant \
--location=$location \
#if $getVar('extra_args', '')
--extra-args="$extra_args" \
#end if
--wait=$wait \
#for $disk in $disks
--disk $disk.disk \
#end for
#for $netif in $networks
--network=$netif.network --mac=$netif.mac \
#end for
--check-cpu \
--noreboot \
--vnc \
--noautoconsole
"""



def run(cmd_str):
	return commands.getstatusoutput(cmd_str)


def load_config(config_path):
    return yaml.load(open(config_path, 'r'))


def compile(tmpl_str, params):
    return Cheetah.Template.Template(source=tmpl_str, searchList=params).respond()


def virtinst_cmd(config_file, site_config=SITE_CONFIG, tmpl=TEMPLATE):
    conf = load_config(site_config)
    conf.update(load_config(config_file))

    return compile(tmpl, conf)


def main():
    parser = optparse.OptionParser("%prog [OPTION ...] CONFIG_FILE")

    parser.add_option('', '--site-conf', help='site config file [%default]', default=SITE_CONFIG)
    parser.add_option('', '--dry-run', help='Dry run mode', default=False, action="store_true")

    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        sys.exit(errno.EINVAL)

    config_file = args[0]

    cmd = virtinst_cmd(config_file, options.site_conf, TEMPLATE)

    if options.dry_run:
        print cmd
    else:
        run(cmd)



if __name__ == '__main__':
    main()

# vim: set sw=4 ts=4 et:

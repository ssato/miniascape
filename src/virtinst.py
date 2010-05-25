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

import errno
import optparse
import os.path
import sys

import miniascape.config

from miniascape.globals import PKG_CONFIG_PATH, PKG_SYSCONFDIR
from miniascape.utils import compile_template, runcmd, load_config



def virtinst_cmd(siteconf, conf, tmpl):
    """Construct a command line to execute virt-install.
    """
    conf = load_config(siteconf)
    conf.update(load_config(conf))

    return compile_template(tmpl, conf)


def main():
    siteconf = os.path.join(PKG_SYSCONFDIR, '/profiles/site.cfg')

    p = optparse.OptionParser("%prog [OPTION ...] PROFILE_CONF")
    p.add_option('-C', '--conf', help='Common config file [%default]', default=PKG_CONFIG_PATH)
    p.add_option('-T', '--template', help='Template file')
    p.add_option('', '--siteconf', help='Common profile data [%default]', default=siteconf)
    p.add_option('', '--dry-run', help='Do not actually perform task', default=False, action="store_true")
    p.add_option('-s', '--silent', help='Silent mode', default=False, action="store_true")
    (options, args) = p.parse_args()

    if len(args) < 1:
        p.print_help()
        sys.exit(errno.EINVAL)

    conf = args[0]
    rc = 0

    c = miniascape.config.init(options.conf)
    virtinst = c.commands.virt_install
    siteconf = c.virtinst.site_config

    if options.template:
        tmpl = options.template
    else:
        tmpl = c.virtinst.template

    cmd = virtinst_cmd(options.siteconf, conf, tmpl)

    if options.dry_run:
        print cmd
    else:
        if not options.silent:
            print cmd

        (rc, out) = runcmd(cmd)
        if rc != 0:
            print >> sys.stderr, out

    sys.exit(rc)


if __name__ == '__main__':
    main()

# vim: set sw=4 ts=4 et:

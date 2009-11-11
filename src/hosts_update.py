#! /usr/bin/python
#
# add / remove host entry into /etc/hosts.
#
# Copyright (C) 2009 Satoru SATOH <satoru.satoh at gmail.com>
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
# @see http://www.augeas.net/tour.html
# @see http://www.augeas.net/docs/api.html
#

import augeas
import errno
import optparse
import sys


def init(root, flags=augeas.augeas.SAVE_BACKUP):
    return augeas.augeas(root, flags=flags)


def ip_match(aug, ip):
    return aug.match("/files/etc/hosts/*[ipaddr = '%s']" % ip)


def ip_remove(aug, ip):
    xs = ip_match(aug, ip)

    if xs:
        for x in xs:
            aug.remove(x)
        aug.save()


def ip_add(aug, ip, fqdn, hostname=False, force=False):
    es = ip_match(aug, ip)

    if es:
        if force:
            ip_remove(aug, ip)
        else:
            sys.exit(errno.EEXIST)

    aug.set('/files/etc/hosts/01/ipaddr', ip)
    aug.set('/files/etc/hosts/01/canonical', fqdn)
    
    if hostname:
        aug.set('/files/etc/hosts/01/alias[1]', hostname)

    aug.save()


def main():
    parser = optparse.OptionParser("%prog [OPTION ...] add IP FQDN | del IP")
    parser.add_option('-r', '--root', default='/', help='use ROOT as the root of the filesystem')
    parser.add_option('', '--force', action="store_true", default=False,
        help='Force adding the host even if exists.')
    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.print_help()
        sys.exit(errno.EINVAL)

    cmd = args[0]
    ip = args[1]

    aug = init(options.root)

    if cmd == 'add':
        if len(args) < 3:
            parser.print_usage()
            sys.exit(errno.EINVAL)

        fqdn = args[2]
        hostname = fqdn.split('.')[0]

        assert fqdn != hostname, "You MUST specify FQDN (not short hostname)!"

        ip_add(aug, ip, fqdn, hostname, options.force)
    
    elif cmd == 'del':
        ip_remove(aug, ip)

    else:
        parser.print_usage()
        sys.exit(errno.EINVAL)


if __name__ == '__main__':
    main()

# vim: set sw=4 ts=4 et:

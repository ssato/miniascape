#! /usr/bin/python
#
# Generate encoded password string to embedded in ks.cfg.
#
# Copyright (C) 2010 Satoru SATOH <satoru.satoh at gmail.com>
#

import errno
import getpass
import optparse
import sys

from miniascape.utils import kickstart_password


def main():
    p = optparse.OptionParser("%prog [OPTION ...] [PASSWORD]")
    p.add_option('-p', '--prompt', action="store_true", default=False, help='Password prompt mode')
    (options, args) = p.parse_args()

    if options.prompt:
        pwd = getpass.getpass()
    else:
        if len(args) < 1:
            p.print_help()
            sys.exit(errno.EINVAL)
        else:
            pwd = args[0]

    print kickstart_password(pwd)


if __name__ == '__main__':
    main()


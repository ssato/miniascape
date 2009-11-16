#! /usr/bin/python
#
# Generate encoded password string to embedded in ks.cfg.
#
# Copyright (C) 2009 Satoru SATOH <satoru.satoh at gmail.com>
#
# License: MIT
#


import crypt
import random
import string
import sys


def encode(s):
    return crypt.crypt(
        s,
        '$1$' + ''.join(
            [random.choice(string.letters + string.digits + './') for i in range(8)]
        )
    )


def main(args=sys.argv):
    if len(args) < 2:
        print >> sys.stderr, "Usage: %s password" % args[0]
        sys.exit(-1)

    print encode(args[1])


if __name__ == '__main__':
    main()


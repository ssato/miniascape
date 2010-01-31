#! /bin/sh
set -e
set -x

autoreconf -vfi
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --sharedstatedir=/var/lib
make

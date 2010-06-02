#! /bin/sh
set -e
set -x

for d in miniascape; do
    autoreconf -vfi
    ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --sharedstatedir=/var/lib
    make
done

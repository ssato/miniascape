#! /bin/sh
set -e
set -x

for d in data tools; do
    autoreconf -vfi
    ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --sharedstatedir=/var/lib
    make
done

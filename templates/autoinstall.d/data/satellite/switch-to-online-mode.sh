#! /bin/sh
set -e
set -x

conf=/etc/rhn/rhn.conf

grep '^disconnected=0' ${conf} > /dev/null 2> /dev/null || \
sed -i.org \
  -e 's/\(.*rhn_parent = \).*/\1satellite.rhn.redhat.com/' \
  -e 's/\(disconnected=\)1/\10/' ${conf}

exit \$?

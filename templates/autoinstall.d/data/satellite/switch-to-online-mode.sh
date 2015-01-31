#! /bin/sh
set -ex

conf=/etc/rhn/rhn.conf

grep '^disconnected=0' ${conf} > /dev/null 2> /dev/null || \
sed -i.save \
  -e 's/\(.*rhn_parent = \).*/\1satellite.rhn.redhat.com/' \
  -e 's/\(disconnected=\)1/\10/' ${conf}

# Satellite 5.7 Installation Guide, 12.5. Automating Synchronization:
# http://red.ht/1zI6UPd
cat << EOF >> /var/spool/cron/root
0 1 * * * perl -le 'sleep rand 9000' && satellite-sync --email >/dev/null 2>/dev/null
EOF

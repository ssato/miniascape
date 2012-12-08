#! /bin/bash
set -e
cconf=/etc/cluster/cluster.conf
if test ! -f $cconf; then
  echo "[Error] Cluster config '$cconf' not found. Prepare it first!"
  exit 1
fi

# Enable cman system service and start it if not running:
/sbin/chkconfig --list cman | grep -q '3:on' || /sbin/chkconfig cman on
/sbin/service cman status || /sbin/service cman start
# vim:sw=2:ts=2:et:

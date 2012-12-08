#! /bin/bash
set -e
cconf=/etc/cluster/cluster.conf
if test ! -f $cconf; then
  echo "[Error] Cluster config '$cconf' not found. Prepare it first!"
  exit 1
fi

# Enable cman system service and start it if not running:
/sbin/chkconfig --list cman | grep -q '3:on' || /sbin/chkconfig cman on
start_cman=${0%/*}/start_cman.sh
if ! `/sbin/service cman status 2>/dev/null >/dev/null`; then
  echo "[Error] Required 'cman' system service NOT running..."
  echo "[Info] Run '$start_cman' on all cluster nodes almost at the same time!"
  exit 1
fi
# vim:sw=2:ts=2:et:

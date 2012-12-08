#! /bin/bash
set -e
if `/sbin/service cman status 2>/dev/null >/dev/null`; then
  # Enable CLVM lock, clvmd system service, and start it if not running:
  grep -q -E '^[ ]+locking_type = 3' /etc/lvm/lvm.conf || lvmconf --enable-cluster
  /sbin/chkconfig --list clvmd | grep -q "3:on" 2>/dev/null || /sbin/chkconfig clvmd on
  /sbin/service clvmd status || /sbin/service clvmd start
else
  echo "[Warn] cman system service does not look running. Check it first"
  exit 1
fi
# vim:sw=2:ts=2:et:

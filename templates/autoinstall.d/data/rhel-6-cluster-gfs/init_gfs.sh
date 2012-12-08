#! /bin/bash
set -e
#set -x

cconf=/etc/cluster/cluster.conf
if test ! -f $cconf; then
  echo "Cluster config '$1' not found. Aborting..."
  exit 1
else
  if `/sbin/service cman status 2>/dev/null >/dev/null`; then
    if `cman_tool status 2>/dev/null >/dev/null`; then
      echo "Cluster looks working. Going forward..."
    else
      echo "Cluster does not look working. Check it before initializing GFS..."
      exit 1
    fi
  else
    echo "CMAN does not look working. Check cluster configuration before initializing GFS..."
    exit 1
  fi
fi

# Enable cman service
/sbin/chkconfig --list cman | grep -q "3:on" 2>/dev/null || /sbin/chkconfig cman on

# Enable CLVM lock, system service (clvmd) and start it if not:
grep -q -E '^[ ]+locking_type = 3' /etc/lvm/lvm.conf 2>/dev/null || \
  lvmconf --enable-cluster
/sbin/chkconfig --list clvmd | grep -q "3:on" 2>/dev/null || /sbin/chkconfig clvmd on
/sbin/service clvmd status || /sbin/service clvmd start
{% import "snippets/pre_post.find_disk" as F -%}
{{ F.find_disk_device(2) }}
diskdev=$1
vg=$2
lv=$3
test "x$diskdev" = "x" && diskdev=/dev/${disk1:?}2
test "x$vg" = "x" && vg={{ cluster.vol.vg|default('gfs-vg-0') }}
test "x$lv" = "x" && lv={{ cluster.vol.lv|default('gfs-lv-0') }}

# Create pv, vg, lv if not exist:
if `pvscan -s | grep -q $diskdev 2>/dev/null > /dev/null`; then
  echo "It looks PV $diskdev already created. Skip this step."
else
  pvcreate $diskdev
fi
if `vgdisplay -s --nosuffix | grep -q "\"$vg\"" 2>/dev/null > /dev/null`; then
  echo "It looks VG $vg already created. Skip this step."
else
  vgcreate -cy $vg $diskdev
fi
if `lvscan -a | grep -q /dev/$vg/$lv 2>/dev/null >/dev/null`; then
  echo "It looks LV $lv already created. Skip this step."
else
  lvcreate -n $lv -l 100%VG $vg && \
    mkfs.gfs2 -t {{ cluster.name }}:{{ cluster.vol.fs }} -j {{ cluster.nodes|length }} -J {{ cluster.vol.journal.size|default('64') }} /dev/$vg/$lv
fi

# vim:sw=2:ts=2:et:

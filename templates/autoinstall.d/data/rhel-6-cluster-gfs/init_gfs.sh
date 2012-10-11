#! /bin/bash
set -ex

# Enable CLVM lock, system service (clvmd) and start it if not:
grep -q -E '^[ ]+locking_type = 3' /etc/lvm/lvm.conf 2>/dev/null || \
  lvmconf --enable-cluster
/sbin/chkconfig --list clvmd | grep -q "3:on" 2>/dev/null || \
  /sbin/chkconfig clvmd on
/sbin/service clvmd status || /sbin/service clvmd start


{% import "snippets/pre_post.find_disk" as F -%}
{{ F.find_disk_device(2) }}

diskdev=$1
vg=$2
lv=$3
test "x$diskdev" = "x" && diskdev=/dev/${disk1:?}2
test "x$vg" = "x" && vg=clustered_vg
test "x$lv" = "x" && lv=clustered_lv

# Create pv, vg, lv if not exist:
pvscan -s | grep -q $diskdev 2>/dev/null || pvcreate $diskdev
vgdisplay -s --nosuffix | grep -q "\"$vg\"" 2>/dev/null || vgcreate -cy $vg $diskdev
lvscan -a | grep -q /dev/$vg/$lv 2>/dev/null || lvcreate -n $lv -l 100%VG $vg

mkfs.gfs2 -t DEMO_GFS_CLUSTER:gfs01 -j {% cluster.nodes|length %} -J 64 /dev/clusteredvg/lv_gfs

# vim:sw=2:ts=2:et:

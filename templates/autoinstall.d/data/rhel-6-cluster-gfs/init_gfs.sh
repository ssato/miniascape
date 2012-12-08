#! /bin/bash
set -e
curdir=${0%/*}
{% import "snippets/pre_post.find_disk" as F -%}
{{ F.find_disk_device(2) }}
diskdev=$1
vg=$2
lv=$3
test "x$diskdev" = "x" && diskdev=/dev/${disk1:?}2
test "x$vg" = "x" && vg={{ cluster.vol.vg|default('gfs-vg-0') }}
test "x$lv" = "x" && lv={{ cluster.vol.lv|default('gfs-lv-0') }}
mkdir /gfs-0
sed -i.save "$ a \
# GFS partitions:\n/dev/$vg/$lv  /gfs-0  gfs2  noatime,nodiratime,noauto,_netdev 0 0" /etc/fstab
{% if cluster_init is defined and cluster_init %}
check_cman=${curdir}/check_cman.sh
start_clvmd=${curdir}/start_clvmd.sh
{% for node in cluster.nodes %}
{%   if loop.first %}bash $check_cman{% else %}ssh root@{{ node.name }} "bash $check_cman"{% endif %}
{% endfor %}
{% for node in cluster.nodes %}
{%   if loop.first %}bash $start_clvmd{% else %}ssh root@{{ node.name }} "bash $start_clvmd"{% endif %}
{% endfor %}
# Create pv, vg, lv if not exist:
pvscan -s | grep -q $diskdev 2>/dev/null > /dev/null || pvcreate $diskdev
vgdisplay -s --nosuffix | grep -q "\"$vg\"" 2>/dev/null > /dev/null || \
  vgcreate -cy $vg $diskdev
lvscan -a | grep -q /dev/$vg/$lv 2>/dev/null >/dev/null || \
  lvcreate -n $lv -l 100%VG $vg && \
    mkfs.gfs2 -t {{ cluster.name }}:{{ cluster.vol.fs }} -j {{ cluster.nodes|length }} -J {{ cluster.vol.journal.size|default('64') }} /dev/$vg/$lv
{%- else -%}
echo "This script should be running on node #1"{% endif %}
# vim:sw=2:ts=2:et:

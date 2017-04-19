#! /bin/bash
#
# It does several things to setup RHUI on RHUA.
#
# Prerequisites:
# - rhui-installer was installed from RHUI ISO image
# - CDSes and LBs (HA Proxy nodes) are ready and accessible with ssh from RHUA w/o password
# - Gluster FS was setup in CDSes and ready to access from RHUA
#
set -ex

cdses="{{ rhui.cdses|join(' ') }}"
cds_0="{{ rhui.cdses|first }}"
cds_rest="{%- for cds in rhui.cdses %}
{%- if not loop.first %}{{ cds }}{% endif %}
{%- endfor %}"
ncdses={{ rhui.cdses|length }}
brick=/export/brick
bricks="{% for cds in rhui.cdses %}{{ cds }}:${brick:?} {% endfor %}"

for cds in ${cdses:?}; do
    ssh ${cds} "yum install -y --enablerepo=rhgs-3.2 glusterfs-{server,cli} rh-rhua-selinux-policy"
    # ssh ... umount /export && mkfs.xfs -f -i size=512 /dev/mapper/vg1-lv_export && mount /export
    ssh ${cds} "systemctl is-active glusterd || (mkdir -p ${brick} && systemctl enable glusterd && systemctl start glusterd)"
done

ssh ${cds_0} "for peer in ${cds_rest:?}; do gluster peer probe \${peer}; done; \
gluster peer status && sleep 10; \
gluster volume create rhui_content_0 replica ${ncdses} ${bricks} && \
gluster volume start rhui_content_0 && \
gluster volume status"

# Client/Server quorum configuration:
# .. seealso:: Red Hat Gluster Storage 3 Admin Guide, 8.10. Managing Split-brain: http://red.ht/2peSXFo
if test $ncdses -le 2; then
    ssh ${cds_0} "gluster volume set rhui_content_0 quorum-type auto"
else
    ssh ${cds_0} "gluster volume set rhui_content_0 quorum-type server; \
gluster volume set all cluster.server-quorum-ratio 51%"
fi

# vim:sw=4:ts=4:et:

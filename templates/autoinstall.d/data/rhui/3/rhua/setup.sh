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

rhui_installer_stamp_dir="/root/setup/rhui-installer.d"
rhui_installer_common_options="--cds-lb-hostname {{ rhui.lb.hostname }} --certs-country {{ rhui.certs.country|default('JP') }} --certs-state {{ rhui.certs.state|default('Tokyo') }} --certs-city {{ rhui.certs.city }} --certs-org '{{ rhui.certs.org }}'"

cdses="{{ rhui.cdses|join(' ') }}"
cds_0="{{ rhui.cdses|first }}"
cds_rest="{%- for cds in rhui.cdses %}
{%- if not loop.first %}{{ cds }}{% endif %}
{%- endfor %}
"
ncdses={{ rhui.cdses|length }}
brick=/export/brick
bricks="{% for cds in rhui.cdses %}{{ cds }}:${brick:?} {% endfor %}"

lbs="{{ rhui.lb.servers|join(' ') if rhui.lb.servers else '' }}"


mkdir -p ${rhui_installer_stamp_dir}
rpm -q rhui-installer || yum install -y rhui-installer

ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
for cds in ${cdses:?}; do
    ssh-copy-id ${cds} && scp /etc/yum.repos.d/*.repo ${cds}:/etc/yum.repos.d/  # .. seealso:: bootstrap.sh
    ssh ${cds} "yum install -y glusterfs-{server,cli} rh-rhua-selinux-policy"
    # ssh ... umount /export && mkfs.xfs -f -i size=512 /dev/mapper/vg1-lv_export && mount /export
    ssh ${cds} "systemctl is-active glusterd || (mkdir -p ${brick} && systemctl enable glusterd && systemctl start glusterd)"
done

ssh ${cds_0} "
for peer in ${cds_rest:?}; do gluster peer probe ${peer}; done
gluster peer status
gluster volume create rhui_content_0 replica ${ncdses} ${bricks}
gluster volume start rhui_content_0
gluster volume status
"
# Client/Server quorum configuration:
# .. seealso:: Red Hat Gluster Storage 3 Admin Guide, 8.10. Managing Split-brain: http://red.ht/2peSXFo
if test $ncdses -le 2; then
    ssh ${cds_0} "gluster volume set rhui_content_0 quorum-type auto"
else
    ssh ${cds_0} "
gluster volume set rhui_content_0 quorum-type server
gluster volume set all cluster.server-quorum-ratio 51%
"
fi

if test "x${lbs}" != x; then
    for lb in ${lbs}; do
        ssh-copy-id ${lb} && scp /etc/yum.repos.d/*.repo ${lb}:/etc/yum.repos.d/
    done
fi

test -f ${rhui_installer_stamp_dir}/${fs}.stamp || \
(rhui-installer ${rhui_installer_common_options} --remote-fs-type=glusterfs --remote-fs-server=${fs}:rhui_content_0 && \
    touch ${rhui_installer_stamp_dir}/${fs}.stamp)

for cds in ${cdses}; do
    rhui cds list -m | grep -E "hostname.: .${cds}" || \
    rhui cds add ${cds} root /root/.ssh/id_rsa -u
done

if test "x${lbs}" != x; then
    for lb in ${lbs}; do
        ssh-copy-id ${lb} && scp /etc/yum.repos.d/*.repo ${lb}:/etc/yum.repos.d/
        rhui haproxy list -m | grep -E "hostname.: .${lb}" || \
        rhui haproxy add ${lb} root /root/.ssh/id_rsa -u
    done
fi

# vim:sw=4:ts=4:et:

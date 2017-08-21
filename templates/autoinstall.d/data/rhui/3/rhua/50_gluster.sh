#! /bin/bash
#
# Setup Gluster Storage on CDS.
#
# Prerequisites:
# - Access to Yum repos of RHEL, RHUI and RH Gluster Storage on CDS
# - SSH access to CDS from RHUA
#
# SEEALSO:
# - RHUI 3.0 System Admin Guide, 5. Shared Storage: http://red.ht/2p8SaYy
# - Red Hat Gluster Storage 3 Admin Guide, 8.10. Managing Split-brain: http://red.ht/2peSXFo
#
set -ex

# CDS_SERVERS, BRICK, CDS_0, CDS_REST, BRICK, NUM_CDS, GLUSTER_BRICKS
source ${0%/*}/config.sh

test "x${RHUI_STORAGE_TYPE:?}" = "xglusterfs" || exit 0

# Install Gluster RPMs, start glusterd and make bricks on CDS
# .. note:: RHEL 7.4 repo must be disabled to install RHGS 3.2 currently (20170811).
cmds="\
yum install -y --enablerepo=rhgs-3.2 --disablerepo=rhel-7.4 glusterfs-{server,cli} rh-rhua-selinux-policy
systemctl is-enabled glusterd 2>/dev/null || systemctl enable glusterd
systemctl is-active glusterd 2>/dev/null || systemctl start glusterd
systemctl status glusterd
mkdir -p ${BRICK:?}
${GLUSTER_ADD_FIREWALL_RULES}
"
for cds in ${CDS_SERVERS:?}; do
    cat << EOC | _ssh_exec_script $cds
${cmds:?}
EOC
done

# Probe Gluster peers on the primary CDS
cmds="\
sleep 5
for peer in "${CDS_REST:?}"; do gluster peer probe \${peer}; done
sleep 5
gluster peer status
sleep 5
"
cat << EOC | _ssh_exec_script ${CDS_0:?}
${cmds:?}
EOC

# Create and start Gluster Storage Volumes
cmds="\
gluster volume info rhui_content_0 || \
(
gluster volume create rhui_content_0 replica ${NUM_CDS:?} ${GLUSTER_BRICKS:?} force && \
gluster volume start rhui_content_0 && \
gluster volume status
)
"
cat << EOC | _ssh_exec_script ${CDS_0:?}
${cmds:?}
EOC

# Configure Gluster Storage Volume Quorum
# "In a three-way replication setup, it is recommended to set
# cluster.quorum-type to auto to avoid split-brains." ( http://red.ht/2uxPjuZ )
test ${NUM_CDS} -eq 3 && _ssh_exec ${CDS_0} 'gluster volume set rhui_content_0 quorum-type auto'
#test ${NUM_CDS} -le 2 || _ssh_exec ${CDS_0} 'gluster volume set rhui_content_0 cluster.server-quorum-type server; gluster volume set all cluster.server-quorum-ratio 51%'
_ssh_exec ${CDS_0} "gluster volume info rhui_content_0"

# vim:sw=4:ts=4:et:

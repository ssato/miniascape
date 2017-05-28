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

# CDS_SERVERS, BRICK, CDS_0, CDS_REST, NUM_CDS, GLUSTER_BRICKS
source ${0%/*}/config.sh

# Install Gluster RPMs, start glusterd and make bricks on CDS
for cds in ${CDS_SERVERS:?}
do
    cat << EOC | ssh -o ConnectTimeout=5 $cds
yum install -y --enablerepo=rhgs-3.2 glusterfs-{server,cli} rh-rhua-selinux-policy
systemctl is-active glusterd || systemctl enable glusterd && systemctl start glusterd
mkdir -p ${BRICK:?}
EOC
done

# Probe Gluster peers on the primary CDS
cat << EOC | ssh -o ConnectTimeout=5 ${CDS_0:?}
for peer in ${CDS_REST:?}; do gluster peer probe \${peer}; done
sleep 5
gluster peer status
EOC
sleep 10

# Create and start Gluster Storage Volumes
cat << EOC | ssh -o ConnectTimeout=5 ${CDS_0:?}
gluster volume create rhui_content_0 replica ${NUM_CDS:?} ${GLUSTER_BRICKS:?} && \
gluster volume start rhui_content_0 && \
gluster volume status
EOC

# Configure Gluster Storage Volume Quorum
test $NUM_CDS -le 2 && \
ssh -o ConnectTimeout=5 ${CDS_0} "gluster volume set rhui_content_0 quorum-type auto" || \
ssh -o ConnectTimeout=5 ${CDS_0} "gluster volume set rhui_content_0 quorum-type server; \
gluster volume set all cluster.server-quorum-ratio 51%"

# vim:sw=4:ts=4:et:

#! /bin/bash
#
# Setup NFS for RHUI servers.
#
# Prerequisites:
# - SSH access to CDS from RHUA
#
# SEEALSO:
# - RHUI 3.0 System Admin Guide, 5. Shared Storage: http://red.ht/2p8SaYy
#
set -ex

# CDS_SERVERS, BRICK, CDS_0, CDS_REST, BRICK, NUM_CDS, GLUSTER_BRICKS
source ${0%/*}/config.sh

cmds="
rpm -q nfs-utils || yum install -y nfs-utils;
setsebool httpd_use_nfs on
"

eval ${cmds:?}
for cds in ${CDS_SERVERS:?}; do _ssh_exec ${cds} 'eval ${cmds}'; done

# vim:sw=4:ts=4:et:

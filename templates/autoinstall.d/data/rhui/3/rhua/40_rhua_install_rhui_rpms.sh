#! /bin/bash
#
# Install RHUI Installer RPM
#
# Prerequisites:
# - Access to yum repos of RHEL, RHUI and RH Gluster Storage
# 
set -ex
source ${0%/*}/config.sh   # RHUI_STORAGE_TYPE

test "${RHUI_STORAGE_TYPE:?}" = "glusterfs" && \
yum install -y --enablerepo=rhgs-3.2 rhui-installer glusterfs-fuse || \
yum install -y rhui-installer

# vim:sw=4:ts=4:et:

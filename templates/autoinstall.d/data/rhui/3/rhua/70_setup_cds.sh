#! /bin/bash
#
# It does several things to setup RHUI on RHUA.
#
# Prerequisites:
# - rhui-installer was installed from RHUI ISO image
# - CDS are ready and accessible with ssh from RHUA w/o password
# - Gluster FS was setup in CDSes and ready to access from RHUA
#
set -ex

# RHUI_AUTH_OPT, CDS_SERVERS
source ${0%/*}/config.sh

rhui_username=admin
rhui_password=$(awk '/rhui_manager_password:/ { print $2; }' /etc/rhui-installer/answers.yaml)
RHUI_AUTH_OPT="--username ${rhui_username:?} --password ${rhui_password:?}"

for cds in ${CDS_SERVERS:?}; do
    rhui ${RHUI_AUTH_OPT:?} cds list -m | grep -E "hostname.: .${cds}" || \
    rhui ${RHUI_AUTH_OPT} cds add ${cds} root /root/.ssh/id_rsa -u
done

# vim:sw=4:ts=4:et:

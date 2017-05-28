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

# RHUI_CERT_NAME, RHUI_AUTH_OPT, RHUI_CERT, RHUI_REPO_IDS
source ${0%/*}/config.sh

RHUI_AUTH_OPT=""  # Force set empty to avoid to password was printed.

rhui_installer_logdir="/root/setup/logs"
rhui_installer_log=${rhui_installer_logdir}/rhui-installer.$(date +%F_%T).log
rhui_installer_stamp=${rhui_installer_logdir}/rhui-installer.stamp

# Upload RHUI entitlement cert
test -f /etc/pki/rhui/redhat/${RHUI_CERT_NAME:?} || \
rhui-manager ${RHUI_AUTH_OPT} cert upload --cert ${RHUI_CERT:?}

# List unused (not added) Yum repos
rhui_repos_list="/root/setup/rhui_repos.txt"
test -f ${rhui_repos_list:?} || \
time rhui-manager ${RHUI_AUTH_OPT} repo unused --by_repo_id | tee ${rhui_repos_list:?}

# Add Yum repos not added yet
f=/tmp/rhui-manager_repo_list.txt
rhui-manager ${RHUI_AUTH_OPT} repo list > $f
repos=""
for rid in ${RHUI_REPO_IDS:?}; do
    grep ${rid} $f || repos="${repos} ${rid}"
done

# It'll take some time to finish the following, e.g. 20 ~ 30 min.
time rhui-manager ${RHUI_AUTH_OPT} repo add_by_repo --repo_ids "$(echo ${repos} | sed 's/ /,/g')"

# vim:sw=4:ts=4:et:

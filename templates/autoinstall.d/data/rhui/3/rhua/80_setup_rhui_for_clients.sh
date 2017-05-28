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

# RHUI_AUTH_OPT, RHUI_CLIENT_CERTS
source ${0%/*}/config.sh

RHUI_CLIENT_WORKDIR=${1:-/root/setup/clients/}

rhui_username=admin
rhui_password=$(awk '/rhui_manager_password:/ { print $2; }' /etc/rhui-installer/answers.yaml)
RHUI_AUTH_OPT="--username ${rhui_username:?} --password ${rhui_password:?}"

# Generate RPM GPG Key pair to sign RHUI client config RPMs built
test -f ~/.rpmmacros || bash -x ${0%/*}/gen_rpm_gpgkey.sh


# List repos available to clients
rhui-manager ${RHUI_AUTH_OPT:?} client labels | sort

mkdir -p ${RHUI_CLIENT_WORKDIR:?}
while read line
do
    test "x$line" = "x" && continue || :
    name=${line%% *}; repos=${line#* }
    rhui-manager ${RHUI_AUTH_OPT} client cert \
        --name ${name:?} --repo_label ${repos:?} \
        --days 3650 --dir ${RHUI_CLIENT_WORKDIR}/
done << EOC
${RHUI_CLIENT_CERTS:?}
EOC

# vim:sw=4:ts=4:et:

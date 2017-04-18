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

lbs="{{ rhui.lb.servers|join(' ') if rhui.lb.servers else '' }}"
rhui_cert="/root/setup/{{ rhui.rhui_entitlement_cert }}"
rhui_repos_list="/root/setup/rhui_repos.txt


mkdir -p ${rhui_installer_stamp_dir}

rhui_installer_log=${rhui_installer_stamp_dir}/installer.log && \
test -f ${rhui_installer_stamp_dir}/rhui-installer.stamp || \
(rhui-installer ${rhui_installer_common_options} \
  --remote-fs-type=glusterfs --remote-fs-server=${cds_0}:rhui_content_0 | tee 2>&1 ${rhui_installer_log} && \
    touch ${rhui_installer_stamp_dir}/rhui-installer.stamp)

set +x

rhui_username=admin
rhui_password=$(sed -nr "s,.* ${rhui_username} / (.+)$,\1,p" ${rhui_installer_log})
rhui_auth_opt="--username ${rhui_username:?} --password ${rhui_password}"
for cds in ${cdses}; do
    rhui ${rhui_auth_opt} cds list -m | grep -E "hostname.: .${cds}" || \
    echo "[Info] Adding CDS: ${cds}"
    rhui ${rhui_auth_opt} cds add ${cds} root /root/.ssh/id_rsa -u
done

rhui-manager ${rhui_auth_opt} cert upload --cert ${rhui_cert:?}
rhui-manager repo unused --by_repo_id | tee ${rhui_repos_list:?}
rhui-manager repo add_by_repo --repo_ids {{ rhui.repos|join(',') }}

# vim:sw=4:ts=4:et:

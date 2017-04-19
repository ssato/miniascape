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

bindir=${0%/*}
rhui_installer_logdir="/root/setup/logs"
rhui_installer_common_options="--cds-lb-hostname {{ rhui.lb.hostname }} --certs-country {{ rhui.certs.country|default('JP') }} --certs-state {{ rhui.certs.state|default('Tokyo') }} --certs-city {{ rhui.certs.city }} --certs-org '{{ rhui.certs.org }}'"

cdses="{{ rhui.cdses|join(' ') }}"
cds_0="{{ rhui.cdses|first }}"

lbs="{{ rhui.lb.servers|join(' ') if rhui.lb.servers else '' }}"
rhui_cert="/root/setup/{{ rhui.rhui_entitlement_cert }}"
rhui_repos_list="/root/setup/rhui_repos.txt"


mkdir -p ${rhui_installer_logdir}

rhui_installer_log=${rhui_installer_logdir}/rhui-installer.$(date +%F_%T).log
test -f ${rhui_installer_logdir}/rhui-installer.stamp || \
(rhui-installer ${rhui_installer_common_options} \
  --remote-fs-type=glusterfs --remote-fs-server=${cds_0}:rhui_content_0 | tee 2>&1 ${rhui_installer_log} && \
    touch ${rhui_installer_logdir}/rhui-installer.stamp)

rhui_username=admin
rhui_password=$(awk '/rhui_manager_password:/ { print $2; }' /etc/rhui-installer/answers.yaml)
rhui_auth_opt="--username ${rhui_username:?} --password ${rhui_password:?}"
for cds in ${cdses}; do
    rhui ${rhui_auth_opt} cds list -m | grep -E "hostname.: .${cds}" || \
    rhui ${rhui_auth_opt} cds add ${cds} root /root/.ssh/id_rsa -u
done

test -f /etc/pki/rhui/redhat/${rhui_cert##*/} || rhui-manager ${rhui_auth_opt} cert upload --cert ${rhui_cert:?}
test -f ${rhui_repos_list:?} || rhui-manager ${rhui_auth_opt} repo unused --by_repo_id | tee ${rhui_repos_list:?}

rhui-manager repo list > /tmp/rhui-manager_repo_list.txt
repos=""
for repo in {{ rhui.repos }}; do
    grep $repo /tmp/rhui-manager_repo_list.txt || repos="${repos} ${repo}"
done
time rhui-manager ${rhui_auth_opt} repo add_by_repo --repo_ids "$(echo ${repos} | sed 's/ /,/g')"

# Generate RPM GPG Key pair to sign built RPMs
bash -x ${bindir}/gen_rpm_gpgkey.sh

# List repos available to clients
rhui-manager ${rhui_auth_opt} client labels | sort

# Generate clinet entitlment certificates and RPMs
{%- for crpm in rhui.client_rpms if crpm.name is defined and crpm.name and
                                    crpm.repos is defined and crpm.repos %}
bash -x ${bindir}/gen_client_rpm.sh -S {{ crpm.name }} {{ crpm.repos|join(' ') }}
{%  endfor %}

# vim:sw=4:ts=4:et:

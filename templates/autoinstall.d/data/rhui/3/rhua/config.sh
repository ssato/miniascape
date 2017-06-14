CURDIR=${0%/*}

function _ssh_exec () { ssh -o ConnectTimeout=5 $@; }
function _ssh_exec_script () { ssh -o ConnectTimeout=5 $1 /bin/bash; }

RHEL_ISO={{ rhui.rhel_iso|default('rhel-server-7.3-x86_64-dvd.iso') }}
RHUI_ISO={{ rhui.rhui_iso|default('RHUI-3.0-RHEL-7-20170321.0-RHUI-x86_64-dvd1.iso') }}  # 2017-03-27
RHGS_ISO={{ rhui.rhgs_iso|default('rhgs-3.2-rhel-7-x86_64-dvd-1.iso') }}

{%- if proxy is defined and proxy.fqdn is defined %}
CURL_PROXY_OPT="--proxy https://{{ proxy.fqdn }}:{{ proxy.port|default("443") }}"
{%-    if proxy.user is defined %}
CURL_PROXY_OPT="${CURL_PROXY_OPT} --proxy-user {{ proxy.user }}:{{ proxy.password }}"
{%-    endif %}
{% endif %}

RHUA={{ rhui.rhua.fqdn }}

CDS_SERVERS="
{%- for cds in rhui.cds.servers -%}
{{      cds.fqdn }}
{%  endfor -%}
"

LB_SERVERS="
{%- for lb in rhui.lb.servers -%}
{{      lb.fqdn }}
{% endfor -%}
"

CDS_0={{ rhui.cds.servers[0].fqdn }}
CDS_REST="
{%- for cds in rhui.cds.servers -%}
{%      if not loop.first %}{{ cds.fqdn }}{% endif %}
{% endfor -%}
"

CDS_LB_HOSTNAME={{ rhui.cds.fqdn }}

NUM_CDS={{ rhui.cds.servers|length }}

# RHUA, CDS and LB will access yum repos via http on this host.
YUM_REPO_SERVER=${CDS_0:?}

# If RHUI_STORAGE_TYPE is Gluster Storage.
BRICK=/export/brick
GLUSTER_BRICKS="
{%- for cds in rhui.cds.servers -%}
{{      cds.fqdn }}:${BRICK:?} {% endfor -%}
"
GLUSTER_FIREWALL_NICS="{{ rhui.storage.interfaces|join(' ')|default('') }}"
test "x${GLUSTER_FIREWALL_NICS}" = "x" || \
GLUSTER_ADD_FIREWALL_RULES="
systemctl is-active firewalld 2>/dev/null && \
(
for nic in ${GLUSTER_FIREWALL_NICS}; do
    zone=\$(firewall-cmd --get-zone-of-interface=\${nic})
    firewall-cmd --add-service=glusterfs --zone=\${zone} --permanent
    firewall-cmd --add-service=glusterfs --zone=\${zone}
done
firewall-cmd --reload
)
"

RHUI_CERT_NAME={{ rhui.rhui_entitlement_cert }}
RHUI_CERT=/root/setup/${RHUI_CERT_NAME:?}

RHUI_STORAGE_TYPE={{ rhui.storage.fstype }}
RHUI_STORAGE_MOUNT={{ rhui.storage.server }}:{{ rhui.storage.mnt }}
RHUI_STORAGE_MOUNT_OPTIONS="{{ rhui.storage.mnt_options|join(',')|default('rw') }}"

RHUI_INSTALLER_TLS_OPTIONS="--certs-country {{ rhui.tls.country|default('JP') }} --certs-state {{ rhui.tls.state|default('Tokyo') }} --certs-city {{ rhui.tls.city }} --certs-org {{ rhui.tls.org }}"
{%- if proxy is defined and proxy.fqdn is defined %}
RHUI_INSTALLER_TLS_OPTIONS="${RHUI_INSTALLER_TLS_OPTIONS:?} --proxy-protocol={{ protocol.protocol|default('http') }} --proxy-hostname={{ proxy.fqdn }} --proxy-port={{ proxy.port|default("443") }}"
{%-    if proxy.user is defined %}
RHUI_INSTALLER_TLS_OPTIONS="${RHUI_INSTALLER_TLS_OPTIONS:?} --proxy-username={{ proxy.user }} --proxy-password={{ proxy.password }}"
{%-    endif %}
{%- endif %}

## Comment out the followings as needed.
#RHUI_USERNAME=admin
#RHUI_PASSWORD=$(awk '/rhui_manager_password:/ { print $2; }' /etc/rhui-installer/answers.yaml || echo '')
#test "x${RHUI_PASSWORD}" = "x" && RHUI_AUTH_OPT="" || \
#RHUI_AUTH_OPT="--username ${RHUI_USERNAME:?} --password ${RHUI_PASSWORD:?}"

RHUI_REPO_IDS="
{%- for repo in rhui.repos if repo.id is defined and repo.id -%}
{{      repo.id }}
{% endfor -%}
"

# Name of RPMs and certs are same.
RHUI_CLIENT_CERTS="
{%- for crpm in rhui.client_rpms -%}
{{      crpm.name }} {{ crpm.repos|join(',') }}
{% endfor -%}
"

# format: <client_rpm_name> <client_rpm_repo_0> [<client_rpm_repo_1> ...] 
RHUI_CLIENT_RPMS="
{%- for crpm in rhui.client_rpms if crpm.name is defined and crpm.name and
                                    crpm.repos is defined and crpm.repos -%}
{{      crpm.name }} {{ crpm.repos|join(' ') }}
{% endfor -%}
"

# vim:sw=4:ts=4:et:

CURDIR=${0%/*}

RHUA={{ rhui.rhua.fqdn }}
REPO_SERVER=${RHUA:?}

CDS_SERVERS="
{% for cds in rhui.cds.servers if cds.fqdn is defined and cds.fqdn %}
{{ cds.fqdn }}
{% endfor %}
"

LB_SERVERS="
{% for lb in rhui.lb.servers if lb.fqdn is defined and lb.fqdn %}
{{ lb.fqdn }}
{% endfor %}
"

CDS_0={% for cds in rhui.cds.servers if cds.fqdn is defined and cds.fqdn %}{% if loop.first %}{{ cds.fqdn }}{% endif %}{% endfor %}
CDS_REST="
{% for cds in rhui.cds.servers if cds.fqdn is defined and cds.fqdn %}
{% if not loop.first %}{{ cds.fqdn }}{% endif %}
{% endfor %}
"

NUM_CDS={{ rhui.cds.servers|length }}

BRICK=/export/brick
GLUSTER_BRICKS="
{% for cds in rhui.cds.servers if cds.fqdn is defined and cds.fqdn %}
{{ cds.fqdn }}:${BRICK:?}
{% endfor %}
"

RHUI_INSTALLER_OPTIONS="
--cds-lb-hostname {{ rhui.lb.hostname }}
--certs-country {{ rhui.tls.country|default('JP') }}
--certs-state {{ rhui.tls.state|default('Tokyo') }}
--certs-city {{ rhui.tls.city }}
--certs-org '{{ rhui.tls.org }}'
"

RHUI_CERT=/root/setup/{{ rhui.rhui_entitlement_cert }}

RHUI_REPO_IDS="
{% for repo in rhui.repos if repo.id is defined and repo.id %}
{{ repo.id }}
{% endfor %}
"

# format: <client_rpm_name> <client_rpm_repo_0> [<client_rpm_repo_1> ...] 
RHUI_CLIENT_RPMS="
{% for crpm in rhui.client_rpms if crpm.name is defined and crpm.name and
                                    crpm.repos is defined and crpm.repos %}
{{ crpm.name }} {{ crpm.repos|join(' ') }}
{% endfor %}
"

# vim:sw=4:ts=4:et:

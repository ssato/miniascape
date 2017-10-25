# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
# Overview of the steps:
#   0. Checks:
#      a. Check FQDN: hostname -f
#      b. Check date and time: date, ntptime, etc.
#
#   1. Installation:
#      a. Satellite RPM Installation: ./install_packages in Satellite ISO image
#      b. Satellite Installation: katello-installer
#
#   2. Setup:
#      a. Setup hammer user configuration and check access: cat ... & hammer ping
#      b. Setup Organization [option; if default organization is not used]: hammer organization create
#      c. Setup Location [option; if default location is not used]: hammer location create
#      d. Upload Satellite manifest: hammer subscription upload
#      e. Setup Lifecycle Environments: hammer lifecycle-environment create
#      f. Setup Yum Repos: hammer repository-set enable
#      g. Setup Sync Plan:
#         - online: hammer sync-plan create --enabled true
#         - offline: hammer sync-plan create --enabled false
#
#      h. Setup Host Collection: hammer host-collection create
#      i. Setup Content View [option]: hammer content-view create, hammer content-view add-repository
#      j. Setup Activation Keys: hammer activation-key create
#      k. Setup Users [option]:
#         - setup LDAP or other auth sources [option]: ex. hammer auth-source ldap create ...
#         - create a user: hammer user create
#
#   3. Sync:
#      a. Check access to CDN: curl https://cdn.redhat.com
#      b. Sync Yum Repos: hammer repository synchronize
#      c. Enable Sync Plan [option: if offline -> online]: hammer sync-plan update --enabled true
#
#   4. Publish & Promote:
#      a. Publish Content Views [option]: hammer content-view publish
#      b. Promote Content Views [option]: hammer content-view version promote
#
#   5. Test clients:
#      a. [client]: Install Satellite SSL CA RPM: yum install -y
#      b. [client]: Register: subscription-manager register
#      c. [satellite]: Check registration of content host: hammer content-host list
#      d. [client]: Test access to Satellite: yum repolist, yum updateinfo list, etc.
#
# References:
#   - https://access.redhat.com/documentation/en/red-hat-satellite/
#   - https://github.com/Katello/hammer-cli-katello/tree/master/lib/hammer_cli_katello
#   - https://access.redhat.com/solutions/1607873
#   - https://access.redhat.com/solutions/1229603
#
CURDIR=${0%/*}
WORKDIR=${CURDIR:?}

LOGDIR=${WORKDIR}/logs

ISO_DIR=${WORKDIR}
RHEL_ISO=$(ls -1 ${ISO_DIR}/rhel*.iso | head -n 1)
SATELLITE_ISO=$(ls -1 ${ISO_DIR}/satellite*.iso | head -n 1)
USE_RPM_INSTALL_SCRIPT=no

SATELLITE_INSTALLER_OPTIONS="
{{- '--foreman-admin-email=%s' % satellite.admin.email|default('root@localhost') }} \
{{  '--foreman-initial-organization=%s' % satellite.organization if satellite.organization }} \
{{  '--foreman-initial-location=%s' % satellite.location if satellite.location }} \
{{ satellite.installer_extra_options|default('') }} \
{% if proxy and proxy.fqdn -%} \
{{     '--katello-proxy-url=http://%s' % proxy.fqdn }} \
--katello-proxy-port={{ proxy.port|default('8080') }} \
{{     '--katello-proxy-username=%s' % proxy.user if proxy.user }} \
{{     '--katello-proxy-password=%s' % proxy.password if proxy.password }} \
{% endif -%}
"

ORG_NAME={{ satellite.organization|default("Default Organization") }}
ORG_LABEL=${ORG_NAME/ /_}
LOC_NAME="Default Location"

ORG_ID_FILE=${HOME}/.hammer/organization_id.txt
HAMMER_ORG_ID_OPT=""
test -f ${ORG_ID_FILE:?} && HAMMER_ORG_ID_OPT="--organization-id $(cat ${ORG_ID_FILE:?})" || :

CURL_PROXY_OPT="-v --cacert /etc/rhsm/ca/redhat-uep.pem --connect-timeout 5"
{% if proxy and proxy.fqdn -%}
PROXY_URL={{ "http://%s:%s" % (proxy.fqdn, proxy.port|default('8080')) }}
CURL_PROXY_OPT="${CURL_PROXY_OPT} --proxy ${PROXY_URL} {{ ' --proxy-user %s:%s' % (proxy.user, proxy.password) if proxy.user and proxy.password }}"
tweak_selinux_policy () {
  semanage port -at foreman_proxy_port_t -p tcp {{ proxy.port|default('8080') }} || :
  katello-service restart
  foreman-rake katello:reindex
}
{% else -%}
tweak_selinux_policy () { :; }
{% endif %}

ENABLE_YUM_REPOS_FOR_CLIENTS="
{% for repo in satellite.repos if repo.name -%}
hammer repository-set enable ${HAMMER_ORG_ID_OPT} --name '{{ repo.name }}' --product '{{ repo.product|default('Red Hat Enterprise Linux Server') }}' {{ '--basearch %s' % repo.arch|default('x86_64') }} {{ '--releasever %s' % repo.releasever if repo.releasever is defined and repo.releasever }}
{% endfor -%}
"

PRODUCTS="
{% for p in satellite.products if p.name -%}
{{      p.name }}
{% endfor -%}
"

CREATE_HOST_COLLECTIONS="
{% for h in satellite.host_collections if h.name -%}
hammer host-collection create ${HAMMER_ORG_ID_OPT} --name '{{ h.name }}' {{ '--max-hosts %s' % h.max if h.max is defined and h.max }} {{ '--hosts %s' % h.hosts|join(',') if h.hosts is defined and h.hosts }}
{% endfor -%}
"

{%  macro _desc_opt(item) -%}
{%    if item and item.description is defined and item.description %}--description '{{ item.description }}'{% endif %}
{%- endmacro %}

CREATE_LIFECYCLE_ENVIRONMENTS="
{% for le in satellite.lifecycle_environments if le.name -%}
hammer lifecycle-environment create ${HAMMER_ORG_ID_OPT} --name '{{ le.name }}' {{ '--prior %s' % le.prior|default('Library') }} {{ _desc_opt(le) }}
{% endfor -%}
"

CREATE_CONTENT_VIEWS="
{% for cv in satellite.content_views if cv.name -%}
hammer content-view create ${HAMMER_ORG_ID_OPT} --name '{{ cv.name }}' {{ _desc_opt(cv) }}
{% endfor -%}
"

ADD_REPOS_TO_CONTENT_VIEWS="
{% for cv in satellite.content_views if cv.name and cv.repos -%}
{%     for repo in cv.repos if repo.name is defined and repo.name and
                               repo.product is defined and repo.product -%}
hammer content-view add-repository ${HAMMER_ORG_ID_OPT} --name '{{ cv.name }}' --product '{{ repo.product }}' --repository '{{ repo.name }}'
{%     endfor -%}
{% endfor -%}
"

CREATE_ACTIVATION_KEYS="
{% for ak in satellite.activation_keys if ak.name -%}
hammer activation-key create ${HAMMER_ORG_ID_OPT} --name '{{ ak.name }}' --content-view '{{ ak.cv|default('Default Organization View') }}' --lifecycle-environment '{{ ak.env|default('Library') }}' {{ '--max-hosts %s' % ak.max if ak.max is defined and ak.max }} {{ _desc_opt(ak) }}
{% endfor -%}
"

ADD_HOST_COLLECTION_TO_ACTIVATION_KEYS="
{% for ak in satellite.activation_keys if ak.name and ak.hc is defined and ak.hc -%}
hammer activation-key add-host-collection ${HAMMER_ORG_ID_OPT} --name '{{ ak.name }}' --host-collection '{{ ak.hc }}'
{% endfor -%}
"

ADD_SUBSCRIPTION_TO_ACTIVATION_KEYS="
{% for ak in satellite.activation_keys if ak.name and
                                          ak.subscription is defined and ak.subscription -%}
hammer activation-key add-subscription ${HAMMER_ORG_ID_OPT} --name '{{ ak.name }}' --subscription-id '{{ ak.subscription }}' --quantity {{ ak.quantity|default('1') }}
{% endfor -%}
"

PRODUCTS_TO_SYNC="
{% for p in satellite.products if p.name and p.sync is defined and p.sync -%}
{{     p.name }}
{% endfor -%}
"

SYNC_BY_REPOS="
{% for p in satellite.products if p.name and
                                   p.repos is defined and p.repos -%}
{%     for r in p.repos if r.name is defined and r.name -%}
hammer repository synchronize ${HAMMER_ORG_ID_OPT} --name '{{ r.name }}' --product '{{ p.name }}' --async
{%     endfor -%}
{% endfor -%}
"
# vim:sw=2:ts=2:et:
{# #}

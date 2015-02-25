# Makefile to setup OpenShift Enterprise brokers and nodes.
# Requirements: curl, etc.
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup

RHN_USERNAME ?= {{ rhn.username if rhn.username }}
RHN_PASSWORD ?= {{ rhn.password if rhn.password }}
RHSM_SUBSCRIPTION_POOL ?= {{ rhn.subscription.pool if rhn.subscription }}

RHSM_REGISTER ?= \
subscription-manager register \
$(if $(RHN_USERNAME),--username=$(RHN_USERNAME),) \
$(if $(RHN_PASSWORD),--password=$(RHN_PASSWORD),) \
--force

RHSM_SUBSCRIBE ?= \
subscription-manager subscribe \
$(if $(RHSM_SUBSCRIPTION_POOL),--pool=$(RHSM_SUBSCRIPTION_POOL),--auto)

RHSM_ACTIVATE_REPOS ?= \
subscription-manager repos \
{% for r in repos -%}
--enable={{ r }} \
{% endfor %}

OPENSHIFT_SH_URL ?= {{ openshift.openshift_sh_url|default('https://raw.githubusercontent.com/openshift/openshift-extras/enterprise-2.2/enterprise/install-scripts/generic/openshift.sh') }}
OPENSHIFT_SH_LOG ?= $(WORKDIR)/log/openshift.sh.log
OPENSHIFT_SH_OPTIONS ?= \
install_method={{ openshift.install_method|default('none') }} \
install_components="{{ openshift.install_components|join(',') }}" \
{% if openshift.install_method == 'rhsm' -%}
rhn_user=$(RHN_USERNAME) rhn_pass=$(RHN_PASSWORD) $(if $(RHSM_SUBSCRIPTION_POOL),sm_reg_pool=$(RHSM_SUBSCRIPTION_POOL),) \
{% endif -%}
domain={{ openshift.domain|default('apps.openshift.example.com') }} \
hosts_domain={{ openshift.hosts_domain|default('openshift.example.com') }} \
broker_hostname={{ openshift.broker_hostname }} \
activemq_hostname={{ openshift.broker_hostname }} \
datastore_hostname={{ openshift.broker_hostname }} \
mcollective_password={{ openshift.mcollective_password|default('rhosesecret') }} \
{% if "named" in openshift.install_components -%}
named_entries="{{ hostname }}:{{ openshift.broker_ip }},broker:{{ openshift.broker_ip }},activemq:{{ openshift.activemq_ip }}{% if openshift.nodes %},{% for node in openshift.nodes if node.hostname and node.ip %}{{ node.hostname }}:{{ node.ip }}{{ ',' if not loop.last }}{% endfor %}{% endif %}" \
{% endif -%}
{% if "broker" in openshift.install_components -%}
{{ 'valid_gear_sizes="%s"' % openshift.valid_gear_sizes if openshift.valid_gear_sizes }} \
{{ "default_gear_size=%s" % openshift.default_gear_size if openshift.default_gear_size }} \
{{ "default_gear_capabilities=%s" % openshift.default_gear_capabilities if openshift.default_gear_capabilities }} \
{%   if openshift.district_mappings -%}
default_districts=false
district_mappings="
{%-    for district, nodes in openshift.district_mappings.iteritems() -%}
{{ district }}:{{ nodes|join(',') }}{{ ';' if not loop.last }}
{%-    endfor %}" \
{%   endif -%}
{% endif -%}
{{ "mongodb_broker_password=%s" % openshift.mongodb_broker_password if openshift.mongodb_broker_password }} \
{{ "openshift_password1=%s" % openshift.openshift_password1 if openshift.openshift_password1 }} \
{% if "node" in openshift.install_components -%}
node_hostname={{ openshift.node_hostname }} \
broker_ip_addr={{ openshift.broker_ip }} \
{{ "node_profile=%s" % openshift.node_profile if openshift.node_profile }} \
{%   if openshift.cartridges -%}
cartridges={{ openshift.cartridges|join(',') }} \
{%   endif -%}
{% endif -%}
$(NULL)


all: setup.stamp

rhsm:
	subscription-manager identity || ($(RHSM_REGISTER) && $(RHSM_SUBSCRIBE))
	subscription-manager repos --disable='*'
	$(RHSM_ACTIVATE_REPOS)
	yum update -y

openshift.sh:
	curl -O $(OPENSHIFT_SH_URL)

setup.stamp: openshift.sh
	test -d $(dir $(OPENSHIFT_SH_LOG)) || mkdir -p $(dir $(OPENSHIFT_SH_LOG))
	bash $< $(OPENSHIFT_SH_OPTIONS) 2>&1 | tee -a $(OPENSHIFT_SH_LOG)
	touch $@

.PHONY: rhsm

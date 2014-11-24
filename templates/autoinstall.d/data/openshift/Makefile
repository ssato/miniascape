# Makefile to setup OpenShift Enterprise brokers and nodes.
# Requirements: curl, etc.
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup

RHN_USERNAME ?= {{ rhn.username if rhn.username else ' # Not set' }}
RHN_PASSWORD ?= {{ rhn.password if rhn.password else ' # Not set' }}
RH_SM_SUBSCRIPTION_POOL ?= {{ rhn.subscription.pool if rhn.subscription and rhn.subscription.pool else 'undef' }}

OPENSHIFT_SH_URL ?= {{ openshift.openshift_sh_url|default('https://raw.githubusercontent.com/openshift/openshift-extras/enterprise-2.2/enterprise/install-scripts/generic/openshift.sh') }}
OPENSHIFT_SH_LOG ?= $(WORKDIR)/log/openshift.sh.log
OPENSHIFT_SH_OPTIONS ?= \
 install_method={{ openshift.install_method|default('rhsm') }} \
 install_components={{ openshift.install_components|join(',') }} \
 domain={{ openshift.domain|default('apps.openshift.example.com') }} \
 hosts_domain={{ openshift.hosts_domain|default('openshift.example.com') }} \
 broker_hostname={{ openshift.broker_hostname }} \
 rhn_user=$(RHN_USERNAME) rhn_pass=$(RHN_PASSWORD) \
 {{ "sm_reg_pool=$(RH_SM_SUBSCRIPTION_POOL)" if '$(RH_SM_SUBSCRIPTION_POOL)' != 'undef' }} \
{% if "named" in openshift.install_components -%}
 named_entries=broker:{{ openshift.broker_ip }},activemq:{{ openshift.activemq_ip }}{% if openshift.nodes %},{% for node in openshift.nodes if node.hostname and node.ip %}{{ node.hostname }}:{{ node.ip }}{{ ',' if not loop.last }}{% endfor %}{% endif %} \
{% endif -%}
{% if "broker" in openshift.install_components -%}
 {{ "valid_gear_sizes=%s" % openshift.valid_gear_sizes if openshift.valid_gear_sizes }} \
 {{ "default_gear_size=%s" % openshift.default_gear_size if openshift.default_gear_size }} \
 {{ "default_gear_capabilities=%s" % openshift.default_gear_capabilities if openshift.default_gear_capabilities }} \
{% endif -%}
 {{ "mcollective_password=%s" % openshift.mcollective_password if openshift.mcollective_password }} \
 {{ "mongodb_broker_password=%s" % openshift.mongodb_broker_password if openshift.mongodb_broker_password }} \
 {{ "openshift_password1=%s" % openshift.openshift_password1 if openshift.openshift_password1 }} \
{% if "node" in openshift.install_components -%}
 node_hostname={{ openshift.node_hostname }} \
 broker_ip_addr={{ openshift.broker_ip }} \
 {{ "node_profile=%s" % openshift.node_profile if openshift.node_profile }} \
 {% if openshift.cartridges %}{{ openshift.cartridges|join(',') }}{% endif %} \
{% endif -%}
$(NULL)


all: setup

openshift.sh:
	curl -O $(OPENSHIFT_SH_URL)

setup: openshift.sh
	test -d $(dir $(OPENSHIFT_SH_LOG)) || mkdir -p $(dir $(OPENSHIFT_SH_LOG))
	bash $< $(OPENSHIFT_SH_OPTIONS) 2>&1 | tee -a $(OPENSHIFT_SH_LOG)

.PHONY: setup

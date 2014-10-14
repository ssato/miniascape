# Makefile to install and setup OpenStack (RDO).
# 
# see also:
# * http://openstack.redhat.com/Neutron-Quickstart
# * http://openstack.redhat.com/Running_an_instance_with_Neutron
# 
WORKDIR ?= /root/setup
FULL_UPDATE ?= no
#
# Required software channels:
#
#   * RDO:
#     - RDO repository (sudo yum install -y https://rdo.fedorapeople.org/rdo-release.rpm)
#     - EPEL 6/7 x86_64
#     - RHEL 6/7 x86_64 Optional
#
#   * RHEL OSP (supported version):
#     - Red Hat Enterprise Linux 7 Server (RPMS): rhel-7-server-rpms [must]
#     - Red Hat OpenStack 5.0 for Server 7 (RPMS): rhel-7-server-openstack-5.0-rpms [must])
#     - Red Hat Common for RHEL Server (RPMS): rhel-7-server-rh-common-rpms [optional; RHEL guest images]
#
# See also:
#   * RHEL-OSP 5 Deploying OpenStack: Proof-of-Concept Environments (PackStack),
#     2.1.2.3.1. Content Delivery Network (CDN) Channels: http://red.ht/1rVMdLv
#   * RDO Repositories: https://openstack.redhat.com/Repositories
#
{% if openstack.use_rdo -%}
make_repos_available ?= yum install -y https://rdo.fedorapeople.org/rdo-release.rpm
{% else %}
RH_SUBSCRIPTION_POOL ?= {{ redhat.subscription.pool|default('') }}

ifeq ($(RH_SUBSCRIPTION_POOL),)
SM_ATTACH_OPTIONS = --auto
else
SM_ATTACH_OPTIONS = --pool=$(RH_SUBSCRIPTION_POOL)
endif

# https://access.redhat.com/products/red-hat-enterprise-linux-openstack-platform/get-started
define make_repos_available ?=
subscription-manager register
subscription-manager attach $(SM_ATTACH_OPTIONS)
subscription-manager repos --disable='*'
subscription-manager repos {% for repo in openstack.repos %} --enable={{ repo }}{% endfor %}
yum-config-manager --setopt=”rhel-7-server-openstack-5.0-rpms.priority=1” --enable rhel-7-server-openstack-5.0-rpms
endef
{% endif %}
install_OPENSTACK_RPMS ?= yum install -y openstack-packstack
packstack_OPTIONS ?= --allinone


all: install

install:
	$(make_repos_available)
ifeq ($(FULL_UPDATE),yes)
	yum update -y
endif
	$(install_OPENSTACK_RPMS)

setup:
	packstack $(packstack_OPTIONS)

#source /root/keystonerc_demo && \
#	  neutron security-group-rule-create --protocol icmp --direction ingress default && \
#	  neutron security-group-rule-create --protocol tcp --port-range-min 22 --port-range-max 22 --direction ingress default

.PHONY: install setup

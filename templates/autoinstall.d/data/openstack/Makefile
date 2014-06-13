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
#     - RHEL 6 x86_64 Optional
#
#   * Red Hat OpenStack (supported version):
#     - RHEL 6 x86_64 Optional
#     - Red Hat OpenStack 3.0 (rhel-x86_64-server-6-ost-3) (Havana not in RHOS yet)
#
RHN_AKEYS ?= {{ rhn.activationkeys|default('') }}
RHN_PROFILENAME ?= {% if rhn.profilename is defined %}{{ rhn.profilename }}{% else %}$(shell hostname -f)_{{ miniascape.builder }}_$(shell date +%Y%m%d_%H%M%S){% endif %}

ifeq ($(RHN_AKEYS),)
rhnreg_ks_OPTIONS ?=
else
rhnreg_ks_OPTIONS ?= --activationkey=$(RHN_AKEYS)
endif

pre_install_OPENSTACK_RPMS ?= yum install -y yum-plugin-priorities
{% if not openstack.use_rdo -%}
make_repos_available ?= test -f /etc/sysconfig/rhn/systemid || rhnreg_ks --profilename=$(RHN_PROFILENAME) -v --force $(rhnreg_ks_OPTIONS)
install_OPENSTACK_RPMS ?= $(make_repos_available) && yum install -y \
python-sphinx python-docutils python-jinja2 \
openstack-keystone openstack-utils openstack-selinux \
openstack-swift-proxy openstack-swift-object openstack-swift-container openstack-swift-account \
openstack-glance \
openstack-cinder \
openstack-quantum openstack-quantum-openvswitch openstack-quantum-linuxbridge \
openstack-nova-novncproxy openstack-nova-console \
openstack-nova-api openstack-nova-compute \
openstack-nova-conductor openstack-nova-scheduler \
python-cinderclient \
openstack-dashboard \
nrpe nagios-plugins-nrpe nagios-plugins-ping \
puppet \
openstack-packstack \
$(NULL)
{% else %}
make_repos_available ?= yum install -y http://rdo.fedorapeople.org/openstack-havana/rdo-release-havana.rpm
install_OPENSTACK_RPMS ?= $(make_repos_available) && yum install -y openstack-packstack
{% endif %}

## TODO: Make the following default for RHOS installation ?
packstack_OPTIONS ?= --allinone --os-quantum-install=n
packstack_OPTIONS ?= --allinone


all: install

install:
	$(make_repos_available)
	$(pre_install_OPENSTACK_RPMS)
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

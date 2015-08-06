# Makefile to install and setup OpenShift Enterprise 3.0 master node.
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
# Overview of the steps after RHEL installation:
#   1. Registration and subscription attachment (master and node)
#   2. Yum repository setup (master and node)
#   3. Install RPMs:
#      a. master: git, etc.
#      b. node: docker, etc.
#   4. Fully update RPMs (master and node)
#   5. Setup Docker and its Storage (node)
#   6. Install and setup OSE with ansible (workstation)
#
# References:
#   - Red Hat OpenShift Enterprise Administrator Guide
#   - Red Hat OpenShift Enterprise Architecture
#   - Red Hat OpenShift Enterprise Getting Started
#
# Load variables, etc.
-include Makefile.custom

# Flags:
IS_MASTER ?= yes
IS_WORKSTATION ?= $(IS_MASTER)
HA_MASTER ?=

CHECK_CLOCK ?= date && chronyc tracking && chronyc sources
CHECK_FQDN ?= \
hostname && hostname -f && hostname -s && \
ping -c1 -w3 localhost && ping -c1 -w3 `hostname -s` && \
ping -c1 -w3 `hostname -f`

CA_CERT ?= /etc/rhsm/ca/redhat-uep.pem
CHECK_CDN_ACCESS ?= \
curl -v --cacert $(CA_CERT) --connect-timeout 5 $(CURL_PROXY_OPT) https://cdn.redhat.com

# Yum repos (software collection) are required anyway:
REGISTER_RHN_IF_NOT ?= \
subscription-manager identity || subscription-manager register $(SUBSCRIPTION_MANAGER_REGISTER_OPTS)

OSE_COMMON_YUM_REPOS ?= \
rhel-7-server-rpms \
rhel-7-server-extras-rpms \
rhel-7-server-optional-rpms \
rhel-7-server-ose-3.0-rpms

OSE_MASTER_YUM_REPOS = $(OSE_COMMON_YUM_REPOS)
ifneq ($(strip $(HA_MASTER)),)
OSE_MASTER_YUM_REPOS += rhel-ha-for-rhel-7-server-rpms
endif

SETUP_NODE_YUM_REPOS ?= \
subscription-manager repos --disable '*' && \
subscription-manager repos $(addprefix --enable=,$(OSE_COMMON_YUM_REPOS))

SETUP_MASTER_YUM_REPOS ?= \
subscription-manager repos --disable '*' && \
subscription-manager repos $(addprefix --enable=,$(OSE_MASTER_YUM_REPOS))

OSE_COMMON_RPMS ?=
OSE_NODE_RPMS ?= $(OSE_COMMON_RPMS) docker
OSE_MASTER_RPMS ?= $(OSE_COMMON_RPMS) wget git net-tools bind-utils iptables-services bridge-utils

ifeq ($(strip $(IS_MASTER)),)
INSTALL_RPMS ?= \
rpm -q $(OSE_NODE_RPMS) || yum install -y $(OSE_NODE_RPMS)
else
INSTALL_RPMS ?= rpm -q $(OSE_MASTER_RPMS) || yum install -y $(OSE_MASTER_RPMS)
endif
FULLY_UPDATE_RPMS = yum update -y

EPEL_RELEASE_RPM_URL ?= https://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm

ifeq ($(strip $(IS_MASTER)$(IS_WORKSTATION)),)
PRE_INSTALL_SETUP ?=
rpm -q docker && \
(grep -qE '^INSECURE_REGISTRY' /etc/sysconfig/docker 2>/dev/null || \
sed -i.save -e "/INSECURE_REGISTRY/a \
INSECURE_REGISTRY='--insecure-registry 172.30.0.0/16'\n" /etc/sysconfig/docker) && \
touch /etc/sysconfig/docker-storage-setup.save && \
echo "VG=vgdocker" >> /etc/sysconfig/docker-storage-setup && \
docker-storage-setup && \
rm -rf /var/lib/docker/* && \
(systemctl is-active docker && systemctl restart docker || :)
else ifeq ($(strip $(IS_WORKSTATION)),)
PRE_INSTALL_SETUP ?= \
(test -f $(HOME)/.ssh/id_rsa || ssh-keygen -t rsa -N '' -f .ssh/id_rsa) && \
for host in $(OSE_MASTER) $(OSE_NODES); do ssh-copy-id $$host; done && \
rpm -q ansible || \
(test -f /etc/yum.repos.d/epel.repo -o -f /etc/fedora-release || \
 (yum install -y $(EPEL_RELEASE_RPM_URL) && \
  sed -i.save -e 's/^(enabled)/(&) = 0/' /etc/yum.repos.d/epel.repo && \
  yum --enablerepo=epel install -y ansible)) && \
(rpm -q ansible || yum install -y ansible) && \
(rpm -q git || yum install -y git) && \
git clone https://github.com/openshift/openshift-ansible openshift-ansible.git
else
PRE_INSTALL_SETUP ?= :
endif

# There are several ways to install and setup OSE 3:
#   a. Quick Installation:
#      x. Run installer available from https://install.openshift.com/ose/
#      y. Run Installation utility available from
#         https://install.openshift.com/portable/oo-install-ose.tgz
#
#   b. Advanced Installation: install and setup with ansbile playbook.
#      OSE playbook is available from https://github.com/openshift/openshift-ansible
#
ifeq ($(strip $(IS_WORKSTATION)),)
OSE_INSTALL ?= :
else
OSE_INSTALL ?= \
cd openshift-ansible.git && git checkout -b 3.x v3.0.0 && \
ansible-playbook -i ../ansible.hosts playbooks/byo/config.yml && \
ssh $(OSE_MASTER) "oc get nodes"
endif


all:
	@echo "Usage: make (check | install-rpms | install | setup)"


check:
	$(CHECK_CLOCK)
	$(CHECK_FQDN)
	$(CHECK_CDN_ACCESS)

install-rpms:
	$(REGISTER_RHN_IF_NOT)
	$(INSTALL_RPMS)
	$(FULLY_UPDATE_RPMS)

install: install.stamp
install.stamp:
	$(PRE_INSTALL_SETUP)
	$(OSE_INSTALL)
	touch $@

.PHONY: check install-rpms install
# vim:noet:

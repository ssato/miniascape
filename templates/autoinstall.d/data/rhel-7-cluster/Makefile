# Makefile to setup pacemaker cluster. DO NOT EDIT THIS!
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#

# NOTE: Every customization should go in it.
-include Makefile.custom

RPMS ?= pcs fence-agents-all

# RHEL 7 High Availability Add-On Administration,
# 2.8. Backing Up and Restoring a Cluster Configuration:
# http://red.ht/1GxBbDy
PCS_BACKUP_FILE ?= pcs-backup-$(shell date +%F_%T)
PCS_DO_BACKUP ?= pcs config backup $(PCS_BACKUP_FILE)

# Firewall configurations:
SETUP_FIREWALL_FOR_FENCE_XVM ?= \
systemctl status firewalld && \
(firewall-cmd --permanent --add-port 1229/tcp && \
 firewall-cmd --add-port 1229/tcp) || \
(systemctl status iptables && \
 iptables -I INPUT  -p tcp -m state --state NEW -m tcp --dport 1229 -j ACCEPT || :)

SETUP_FIREWALL_FOR_HA_CLUSTER ?= \
systemctl status firewalld && \
  (firewall-cmd --permanent --add-service=high-availability && \
   firewall-cmd --add-service=high-availability && \
   firewall-cmd --permanent --add-port 2224/tcp && \
   firewall-cmd --add-port 2224/tcp) || \
(systemctl status iptables && \
 (iptables -I INPUT  -p udp --dport 5405 -j ACCEPT && \
  iptables -I INPUT  -p tcp --dport 2224 -j ACCEPT && \
  iptables -I INPUT  -p tcp -m state --state NEW -m tcp --dport 2224 -j ACCEPT) || :)

ENSURE_PCSD_STARTED ?= \
(systemctl is-enabled pcsd || systemctl enable pcsd) && \
(systemctl is-active pcsd || systemctl start pcsd); \
systemctl status pcsd

# see: pcs(8)
ifeq ($(PCS_CLUSTER_NODES),)
PCS_AUTH_ALL = echo "PCS_CLUSTER_NODES is not set. Aborting ..."; exit 1
else
PCS_AUTH_ALL = \
test -f /var/lib/pcsd/tokens || \
pcs cluster auth -u hacluster -p $(PCS_PASSWORD) $(PCS_CLUSTER_NODES)
endif

PCS_SETUP_START = \
pcs cluster status || \
pcs cluster setup --start --name $(PCS_CLUSTER_NAME) $(PCS_CLUSTER_NODES)


all:
	@echo "Usage: make [VAR_OVERRIDES ...]"
	@echo ""
	@echo "ex. make PASSWORD=secret***"
	@echo "ex. make install"
	@echo ""
	@echo "  Targets: install prep setup"

install: $(WORKDIR)/install.stamp
$(WORKDIR)/install.stamp:
	rpm -q $(RPMS) || yum install -y $(RPMS)
	touch $@

# RHEL 7 High Availability Add-On Administration,
# - Chapter 1. Creating a Red Hat High-Availability Cluster with Pacemaker:
#   http://red.ht/1T8SX3C
# - Chapter 11. The pcsd Web UI: http://red.ht/1cKGqSD
prep: $(WORKDIR)/prep.stamp
$(WORKDIR)/prep.stamp: $(WORKDIR)/install.stamp
	echo $(PCS_PASSWORD) | passwd hacluster --stdin --force
	$(SETUP_FIREWALL_FOR_FENCE_XVM)
	$(SETUP_FIREWALL_FOR_HA_CLUSTER)
	$(ENSURE_PCSD_STARTED)
	touch $@

# RHEL 7 High Availability Add-On Administration, 1.2. Cluster Creation:
# http://red.ht/1dtvh9p
create-cluster: $(WORKDIR)/create-cluster.stamp
$(WORKDIR)/create-cluster.stamp: $(WORKDIR)/prep.stamp
	$(PCS_AUTH_ALL)
	$(PCS_SETUP_START)
	$(PCS_SETUP_INIT)
	pcs cluster enable --all
	pcs cluster status
	touch $@

# FIXME:
# - RHEL 7 High Availability Add-On Administration, 1.3. Fencing Configuration:
#   http://red.ht/1S1ywEe
# - `pcs stonith describe fence_xvm`
# - How can I avoid having to create a stonith device for each node in a
#   cluster where the "port" (-n) values do not match the node names in RHEL 6
#   or 7 with pacemaker?: https://access.redhat.com/solutions/701463
setup-fences: $(WORKDIR)/setup-fences.stamp
$(WORKDIR)/setup-fences.stamp: $(WORKDIR)/create-cluster.stamp
	pcs stonith show --all
	pcs property show --full
ifeq ($(PCS_SETUP_FENCES),)
	echo "PCS_SETUP_FENCES is not set. Aborting ..."; exit 1
else
	$(PCS_SETUP_FENCES)
endif
	pcs stonith show --all
	pcs property show --full
	pcs property set stonith-enabled=true
	pcs cluster status
	$(PCS_DO_BACKUP)
	touch $@

setup-resources: $(WORKDIR)/setup-resources.stamp
$(WORKDIR)/setup-resources.stamp: $(WORKDIR)/setup-fences.stamp
ifeq ($(PCS_SETUP_RESOURCES),)
	echo "PCS_SETUP_RESOURCES is not set. Aborting ..."; exit 1
else
	$(PCS_SETUP_RESOURCES)
endif
ifneq ($(PCS_SETUP_CONSTRAINTS),)
	$(PCS_SETUP_CONSTRAINTS)
endif
	pcs resource show --full
	pcs cluster status
	$(PCS_DO_BACKUP)
	touch $@

setup: $(WORKDIR)/setup-resources

.PHONY: install prep create-cluster setup-fences setup-resources setup
{# -#}

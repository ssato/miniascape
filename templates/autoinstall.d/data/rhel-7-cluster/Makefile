# Makefile to setup pacemaker cluster. DO NOT EDIT THIS!
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#

# NOTE: Every customization should go in it.
-include Makefile.custom

RPMS ?= pcs fence-agents-all
OPEN_CLUSTER_PORTS = \
systemctl status firewalld && \
  (firewall-cmd --permanent --add-service=high-availability; \
   firewall-cmd --add-service=high-availability; \
   firewall-cmd --permanent --add-port 1229/tcp; \
   firewall-cmd --add-port 1229/tcp) || \
systemctl status iptables && \
  (iptables -I INPUT  -p tcp -m state --state NEW -m tcp --dport 1229 -j ACCEPT; \
   iptables -I INPUT  -p udp --dport 5405 -j ACCEPT; \
   iptables -I INPUT  -p tcp -m state --state NEW -m tcp --dport 2224 -j ACCEPT) || :


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

prep: $(WORKDIR)/prep.stamp
$(WORKDIR)/prep.stamp: $(WORKDIR)/install.stamp
	echo $(PASSWORD) | passwd hacluster --stdin --force
	$(OPEN_CLUSTER_PORTS)
	systemctl enable pcsd && systemctl start pcsd && systemctl pcsd start
	touch $@

# - RHEL 7 HA Addon Admin Guide, 1.1. Cluster software installation:
#   http://red.ht/1AiWJ4k
setup-cluster: $(WORKDIR)/setup-cluster.stamp
$(WORKDIR)/setup-cluster.stamp: $(WORKDIR)/prep.stamp
	pcs cluster status || pcs cluster start --all
	pcs cluster setup --start --name $(PCS_CLUSTER_NAME) $(SETUP_FORCE) $(PCS_CLUSTER_NODES)
	pcs cluster auth -u hacluster -p $(PASSWORD) $(SETUP_FORCE) $(PCS_CLUSTER_NODES)
	pcs cluster enable --all
	pcs cluster status
	touch $@


# - How can I avoid having to create a stonith device for each node in a
#   cluster where the "port" (-n) values do not match the node names in RHEL 6
#   or 7 with pacemaker?: https://access.redhat.com/solutions/701463
setup-fences: $(WORKDIR)/setup-fences.stamp
$(WORKDIR)/setup-fences.stamp: $(WORKDIR)/setup-cluster.stamp
	pcs property show --full
	pcs stonith create $(PCS_FENCE_DEV_NAME) fence_virt \
		pcmk_host_check="static-list" pcmk_host_list="$(PCS_FENCE_HOST_LIST)" \
		pcmk_host_map="$(PCS_FENCE_HOST_MAP)"
	pcs property set stonith-enabled=true
	pcs property show --full
	pcs cluster status
	touch $@

setup-resources: $(WORKDIR)/setup-resources.stamp
$(WORKDIR)/setup-resources.stamp: $(WORKDIR)/setup-fences.stamp
	$(PCS_SETUP_RESOURCES)
	pcs resource show --full
	pcs cluster status
	touch $@

# TODO: Setup typical constraints
setup-services: $(WORKDIR)/setup-services.stamp
$(WORKDIR)/setup-services.stamp: $(WORKDIR)/setup-resources.stamp
	$(PCS_SETUP_SERVICES)
	pcs cluster status
	touch $@

setup: $(WORKDIR)/setup-services

.PHONY: install prep setup-cluster setup-fences setup-resources setup-services setup

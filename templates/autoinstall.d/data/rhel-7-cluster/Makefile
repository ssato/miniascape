# Makefile to setup pacemaker (pcs, etc.)
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup

PASSWORD ?= {{ m2_random_string() if m2_random_string is defined else 'SeCrEt0237' }}
RPMS ?= pcs fence-agents-all


all:
	@echo "Usage: make [VAR_OVERRIDES ...]"
	@echo ""
	@echo "ex. make PASSWORD=secret***"
	@echo "ex. make install"
	@echo ""
	@echo "  Targets: fetch install setup"

install: $(WORKDIR)/install.stamp
$(WORKDIR)/install.stamp:
	rpm -q $(RPMS) || yum install -y $(RPMS)
	touch $@

# RHEL 7 HA Addon Admin Guide, 1.1. Cluster software installation:
# http://red.ht/1AiWJ4k
setup: $(WORKDIR)/setup.stamp
$(WORKDIR)/setup.stamp: $(WORKDIR)/install.stamp
	echo $(PASSWORD) | passwd hacluster --stdin --force
	systemctl enable pcsd && systemctl start pcsd && systemctl pcsd start
	pcs cluster start -all
	pcs cluster setup {{ cluster.name|default('examplecluster') }} \
		{{ cluster.nodes|join(' ') }}
	pcs cluster auth {{ cluster.nodes|join(' ') }}
	pcs cluster setup --start --name {{ cluster.nodes|join(' ') }}
	pcs cluster enable --all
	pcs stonith create {{ cluster.name|default('examplecluster') }} \
		fence_virt params \
		pcmk_host_check="static-list" \
		pcmk_host_map="{{ cluster.nodes|join(';') }}" \
		pcmk_host_list="{{ cluster.nodes|join(',') }}"
	{% for res in cluster.resources if res.name and res.type and res.params -%}
	pcs resource create {{ res.name }} {{ res.type }} \
		{% for key, val in res.params %}{{ key }}="{{ val }}" {% endfor %}; \
	{% endfor %}
	{% for svc in cluster.services if svc.name and svc.resources -%}
	pcs resource group add {{ svc.name }} {{ svc.resouces|join(' ') }}; \
	{% endfor %}
	{% for constraint in cluster.constraints if constraint.service and constraint.prefers -%}
	pcs constraint location {{ constraint.service }} prefers {{ constraint.prefers }}; \
	{% endfor %}
	pcs cluster status
	touch $@

.PHONY: install setup

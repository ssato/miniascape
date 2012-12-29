# Makefile to install and setup JBoss
# Author: Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup

JBOSS_CONF_DIR ?= /etc/jbossas/domain

FULL_UPDATE ?= no

#
# Prepare activation keys which required software channels below
# to install JBoss RPMs from RHN.
#
# Required software channels: jbappplatform-6-x86_64-server-6-rpm
#
RHN_AKEYS ?= {{ rhn.activationkeys }}
RHN_PROFILENAME ?= {% if rhn.profilename is defined %}{{ rhn.profilename }}{% else %}$(shell hostname -f)_$(shell date +%Y%m%d_%H_%M_%S){% endif %}

INSTALL_DATA = install -m 644

{% if jboss.is_domain_controller is defined and jboss.is_domain_controller %}
# Domain Controller:
# domain.xml: Use custom one; added <server-groups/> as needed
# host.xml: Use /etc/jbossas/domain/host-master.xml by jbossas-domain RPM w/o
#           any modifications.
define install_conf =
$(INSTALL_DATA) $(JBOSS_CONF_DIR)/domain-0.xml $(JBOSS_CONF_DIR)/
sed -i.save -e '$ a \
JBOSS_SERVER_CONFIG="domain-0.xml"\nJBOSS_HOST_CONFIG="host-master.xml"\n' /etc/sysconfig/jbossas-domain
sed -i.save -e '$ a \
admin={{ jboss.secret.hash }}\n' $(JBOSS_CONF_DIR)/mgmt-users.properties
endef
{% else %}
# Slave servers in domain:
# host.xml: Use custom one; updated <secret/> and <servers/>, etc.
define install_conf =
$(INSTALL_DATA) $(JBOSS_CONF_DIR)/host-slave-0.xml $(JBOSS_CONF_DIR)/
sed -i.save -e '$ a \
JBOSS_HOST_CONFIG="host-slave-0.xml"\n' /etc/sysconfig/jbossas-domain
endef
{% endif %}
# @se http://red.ht/WLUrCu
install: $(WORKDIR)/install.stamp
$(WORKDIR)/install.stamp:
	test -f /etc/sysconfig/rhn/systemid || rhnreg_ks --profilename=$(RHN_PROFILENAME) -v --activationkey=$(RHN_AKEYS) --force
ifeq ($(FULL_UPDATE),yes)
	yum -y update && yum groupinstall -y jboss-eap6
else
	yum groupinstall -y jboss-eap6
endif
	touch $@

setup: $(WORKDIR)/setup.stamp
$(WORKDIR)/setup.stamp: $(WORKDIR)/install.stamp
	$(install_conf)
	chkconfig jbossas-domain on
	touch $@

.PHONY: install setup

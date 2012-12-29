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

define update_domain_and_host_xml =
test -f $(WORKDIR)/host.xml && cp $(JBOSS_CONF_DIR)/host.xml $(JBOSS_CONF_DIR)/host.xml.save && cp $(WORKDIR)/host.xml $(JBOSS_CONF_DIR)/
test -f $(WORKDIR)/domain.xml && cp $(JBOSS_CONF_DIR)/domain.xml $(JBOSS_CONF_DIR)/domain.xml.save && cp $(WORKDIR)/domain.xml $(JBOSS_CONF_DIR)/
endef


# @se http://red.ht/WLUrCu
install: $(WORKDIR)/install.stamp
$(WORKDIR)/install.stamp:
	test -f /etc/sysconfig/rhn/systemid || rhnreg_ks --profilename=$(RHN_PROFILENAME) -v --activationkey=$(RHN_AKEYS) --force
ifeq ($(FULL_UPDATE),yes)
	yum -y update
else
	yum repolist
endif
	yum groupinstall -y jboss-eap6
	touch $@

setup: $(WORKDIR)/setup.stamp
$(WORKDIR)/setup.stamp: $(WORKDIR)/install.stamp
	$(update_domain_and_host_xml)
	touch $@

.PHONY: install setup

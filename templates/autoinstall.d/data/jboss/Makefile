# Makefile to install and setup JBoss
# Author: Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup

#
# Prepare activation keys which required software channels below
# to install JBoss RPMs from RHN.
#
# Required software channels: jbappplatform-6-x86_64-server-6-rpm
#
RHN_AKEYS ?= {{ rhn.activationkeys }}
RHN_PROFILENAME ?= {% if rhn.profilename is defined %}{{ rhn.profilename }}{% else %}$(shell hostname -f)_$(shell date +%Y%m%d_%H_%M_%S){% endif %}

# @se http://red.ht/WLUrCu
install: $(WORKDIR)/install.stamp
$(WORKDIR)/install.stamp:
	test -f /etc/sysconfig/rhn/systemid || rhnreg_ks --profilename=$(RHN_PROFILENAME) -v --activationkey=$(RHN_AKEYS) --force
	yum -y update
	yum groupinstall -y jboss-eap6
	touch $@

setup: $(WORKDIR)/setup.stamp
$(WORKDIR)/setup.stamp: $(WORKDIR)/install.stamp
	update_domain_and_host_xml
	touch $@

.PHONY: install setup

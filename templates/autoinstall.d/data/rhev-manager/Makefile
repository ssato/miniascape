# Makefile to install and setup RHEV-M
# Author: Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup

ANSTXT ?= $(WORKDIR)/answers.txt

#
# Prepare activation keys which required software channels below
# to install rhevm RPMs from RHN.
#
# Required software channels: jbappplatform-6-x86_64-server-6-rpm,
# 	rhel-x86_64-server-6, rhel-x86_64-server-6-rhevm-3.1,
# 	rhel-x86_64-server-supplementary-6, rhel-x86_64-server-6-rhevh
#
RHN_AKEYS ?= {{ rhn.activationkeys }}
RHN_PROFILENAME ?= {% if rhn.profilename is defined %}{{ rhn.profilename }}{% else %}$(shell hostname -f)_$(shell date +%Y%m%d_%H_%M_%S){% endif %}

# http://red.ht/UKeD47
define rhn_register =
#subscription-manager register --username={{ rhn.username }} --password={{ rhn.password }} --autosubscribe --force
subscription-manager register --autosubscribe --force
yum-config-manager --enablerepo=jbappplatform-6-x86_64-server-6-rpm --enablerepo=rhel-x86_64-server-6-rhevm-3.1 --enablerepo=rhel-x86_64-server-supplementary-6
endef


install: $(WORKDIR)/install.stamp
$(WORKDIR)/install.stamp:
	test -f /etc/sysconfig/rhn/systemid || rhnreg_ks --profilename=$(RHN_PROFILENAME) -v --activationkey=$(RHN_AKEYS) --force
	yum -y update
	rpm -q rhevm || yum -y install rhevm
	touch $@

setup: $(WORKDIR)/setup.stamp
$(WORKDIR)/setup.stamp: $(ANSTXT)
	rhevm-setup --gen-answer-file=$(ANSTXT).header
	cat $(ANSTXT).header $(ANSTXT) > $(ANSTXT).new
	rhevm-setup --answer-file=$(ANSTXT).new
	touch $@

.PHONY: install

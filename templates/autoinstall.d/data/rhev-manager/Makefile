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
# 	and rhel-x86_64-server-supplementary-6
#
RHN_AKEYS ?= {{ rhn.activationkeys }}
RHN_PROFILENAME ?= {% if rhn.profilename is defined %}{{ rhn.profilename }}{% else %}$(shell hostname -f)_$(shell date +%Y%m%d_%H_%M_%S){% endif %}


install: $(WORKDIR)/install.stamp
$(WORKDIR)/install.stamp:
	test -f /etc/sysconfig/rhn/systemid || rhnreg_ks --profilename=$(RHN_PROFILENAME) -v --activationkey=$(RHN_AKEYS) --force
	yum -y update
	rpm -q rhevm || yum -y install rhevm
	touch $@

setup: $(WORKDIR)/setup.stamp
$(WORKDIR)/setup.stamp: $(ANSTXT)
	rhevm-setup --answer-file=$<
	touch $@

.PHONY: install

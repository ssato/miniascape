# Makefile to install RHUI RPMs into CDS and setup it.
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup
FQDN ?= {{ fqdn }}

# @see http://red.ht/RAKEyc :
RHUI_ISO ?= $(WORKDIR)/RHEL-6-RHUI-2-LATEST-Server-x86_64-DVD.iso
GPG_PUB_KEY ?= $(WORKDIR)/RPM-GPG-KEY-rhui-custom
RHUI_CONFIG_RPM ?= $(wildcard $(WORKDIR)/rh-{{ hostname }}-config-*.el6.noarch.rpm)


all: check install

check: $(WORKDIR)/check.stamp
$(WORKDIR)/check.stamp:
	date
	fqdn=`hostname -f`; test "x$(FQDN)" != "x" -a "x$$fqdn" = "x$(FQDN)"
	test -f check.sh && bash -x ./check.sh || :
	touch $@

install: $(WORKDIR)/install-cds.stamp
$(WORKDIR)/install-cds.stamp: $(RHUI_ISO)
	mount -o ro,loop $(RHUI_ISO) /mnt
	cd /mnt && ./install_CDS.sh && cd - && umount /mnt
	touch $@

setup:
	rpm -q pulp-cds
	install -m 644 $(GPG_PUB_KEY) /etc/pki/rpm-gpg/
	rpm --import /etc/pki/rpm-gpg/$(notdir $(GPG_PUB_KEY))
	test -f $(RHUI_CONFIG_RPM)
	rpm --checksig $(RHUI_CONFIG_RPM)
	yum install -y $(RHUI_CONFIG_RPM)
	service pulp-cds status
	service pulp-cds restart

.PHONY: check install setup

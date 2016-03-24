# Makefile to install RHUI RPMs in CDS.
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup
FQDN ?= {{ fqdn }}

# @see http://red.ht/RAKEyc :
RHUI_ISO ?= $(WORKDIR)/RHEL-6-RHUI-2-LATEST-Server-x86_64-DVD.iso

all: check install

check: $(WORKDIR)/check.stamp
$(WORKDIR)/check.stamp:
	date
	fqdn=`hostname -f`; test "x$(FQDN)" != "x" -a "x$$fqdn" = "x$(FQDN)"
	touch $@

install: $(WORKDIR)/install-cds.stamp
$(WORKDIR)/install-cds.stamp: $(RHUI_ISO)
	mount -o ro,loop $(RHUI_ISO) /mnt
	cd /mnt && ./install_CDS.sh && cd - && umount /mnt
	touch $@

.PHONY: check install

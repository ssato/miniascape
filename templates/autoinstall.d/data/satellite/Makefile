# Makefile to install RHN Satellite
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup

SATELLITE_ISO ?= $(WORKDIR)/satellite-5.5.0-20120911-rhel-6-x86_64.iso
ANSTXT ?= $(WORKDIR)/answers.txt

EXTRA_INSTALLER_OPTS ?= --disconnected


all: check install

check: $(WORKDIR)/check.stamp
$(WORKDIR)/check.stamp:
	date
	fqdn=`hostname -f`; test "x$$fqdn" = 'x{{ fqdn }}'
	touch $@

install: $(WORKDIR)/install.stamp
$(WORKDIR)/install.stamp: $(SATELLITE_ISO)
	mount -o ro,loop $(SATELLITE_ISO) /mnt
	cd /mnt && ./install.pl --answer-file=$(ANSTXT) $(EXTRA_INSTALLER_OPTS) && cd - && umount /mnt
	touch $@

.PHONY: check install


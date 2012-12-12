# Makefile to fetch RHDS DVD iso image, install and setup it.
# Requirements: curl or wget, RHDS DVD iso image, etc.
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup

# How to get RHDS Installation ISO -> http://red.ht/XRBXnz
INSTALLATION_ISO ?= DSRV-9-x86_64-DVD1.iso
ISO_URL ?= {{ instal_iso_url }}

SETUP_INF ?= $(WORKDIR)/setup.inf

FETCH_PROG ?= wget
ifeq ($(FETCH_PROG),curl)
fetch_ISO = curl -v --insecure -O
else
fetch_ISO = wget --no-check-certificate
endif


all:
	@echo "Usage: make [VAR_OVERRIDES ...]"
	@echo ""
	@echo "ex. make ISO_URL=http://example.com/rhds.iso fetch_ISO='curl -O ' fetch"
	@echo "ex. make install"
	@echo ""
	@echo "  Targets: fetch install setup"

# common:
fetch: $(WORKDIR)/$(INSTALLATION_ISO)
$(WORKDIR)/$(INSTALLATION_ISO):
	$(fetch_ISO) $(ISO_URL)

# see also: http://red.ht/XRBXnz
install: $(WORKDIR)/install.stamp
$(WORKDIR)/install.stamp: $(INSTALLATION_ISO)
	mount -o ro,loop $(RHUI_ISO) /mnt
	cd /mnt && yum install -y `ls /mnt/Packages/*.rpm | egrep -iv -e devel -e debuginfo`
	cd - && umount /mnt
	touch $@

setup: $(WORKDIR)/setup.stamp
$(WORKDIR)/setup.stamp: $(WORKDIR)/install.stamp $(SETUP_INF)
	/usr/sbin/setup-ds-admin.pl -s -f $(SETUP_INF)
	touch $@

.PHONY: fetch install setup

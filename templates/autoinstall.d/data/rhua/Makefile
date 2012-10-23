# Makefile to fetch RHUI DVD iso image, install RHUI and generate certs.
# Requirements: openssl, curl
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup

# @see http://red.ht/RAKEyc :
RHUI_ISO ?= RHEL-6-RHUI-2-LATEST-Server-x86_64-DVD.iso
RHUI_URL ?= https://cdn.redhat.com/content/dist/rhel/rhui/server/6/6Server/x86_64/rhui/2/iso/$(RHUI_ISO)

fetch_RHUI_ISO = curl --cert {{ rhui_entitlement_certs[0] }}
{% if proxy is defined and proxy.fqdn is defined %}fetch_RHUI_ISO += --proxy https://{{ proxy.fqdn }}:{{ proxy.port|default("443") }} {% if proxy.user is defined %}--proxy-user {{ proxy.user }}:{{ proxy.password }}{% endif %}{% endif %}
fetch_RHUI_ISO += -v --insecure


all:
	@echo "Usage: make [VAR_OVERRIDES ...]"
	@echo ""
	@echo "ex. make RHUI_URL=http://example.com/rhui.iso fetch_RHUI_ISO='curl ' fetch"
	@echo "ex. make install-rhua"
	@echo ""
	@echo "  Targets for RHUA: fetch install-rhua certs genconf"
	@echo "  Targets for CDS : fetch install-cds"

# common:
fetch: $(RHUI_ISO)
$(RHUI_ISO):
	$(fetch_RHUI_ISO) $(RHUI_URL) > $@.tmp
	mv $@.tmp $@

# On RHUA
install-rhua: install-rhua.stamp
install-rhua.stamp: $(RHUI_ISO)
	mount -o ro,loop $(RHUI_ISO) /mnt
	cd /mnt && ./install_RHUA.sh && cd - && umount /mnt
	touch $@

certs: certs.stamp
certs.stamp:
	make -C $(WORKDIR)/certs
	touch $@

genconf: genconf.stamp
genconf.stamp: certs.stamp install-rhua.stamp $(WORKDIR)/answers.txt
	rhui-installer $(WORKDIR)/answers.txt 2>&1 | tee $(WORKDIR)/rhui-install.log

# On CDS:
install-cds: install-cds.stamp
install-cds.stamp: $(RHUI_ISO)
	mount -o ro,loop $(RHUI_ISO) /mnt
	cd /mnt && ./install_CDS.sh && cd - && umount /mnt
	touch $@

.PHONY: fetch install-rhua certs genconf install-cds

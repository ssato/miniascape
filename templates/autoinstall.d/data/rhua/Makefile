# Makefile to fetch RHUI DVD iso image, install RHUI and generate certs.
# Requirements: openssl, curl
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#

# @see http://red.ht/RAKEyc :
RHUI_ISO ?= RHEL-6-RHUI-2-LATEST-Server-x86_64-DVD.iso
RHUI_URL ?= https://cdn.redhat.com/content/dist/rhel/rhui/server/6/6Server/x86_64/rhui/2/iso/$(RHUI_ISO)

rhui_crt=/root/setup/rhui_entitlement_certs/70154042338280.pem
if test \$# -gt 0; then rhui_crt=\$1; fi

fetch_RHUI_ISO = curl --cert {{ rhui_entitlement_cert }} \
  {% if proxy is defined %}--proxy https://{{ proxy.fqdn }}:{{ proxy.port|default("443") }} \
  {% if proxy.user is defined %}--proxy-user {{ proxy.user }}:{{ proxy.password }}{% endif %}{% endif %} \
  -v --insecure


all:
	@echo "Usage: make [VAR_OVERRIDES ...]"
	@echo ""
	@echo "ex. make RHUI_URL=http://example.com/rhui.iso fetch_RHUI_ISO='curl ' fetch"
	@echo "ex. make install-rhua"

fetch: $(RHUI_ISO)
$(RHUI_ISO):
	$(fetch_RHUI_ISO) $(RHUI_URL) > $@.tmp
	mv $@.tmp $@

install-rhua: $(RHUI_ISO)
	mount -o ro,loop $(RHUI_ISO) /mnt
	cd /mnt && ./install_RHUA.sh && cd - && umount /mnt

install-cds: $(RHUI_ISO)
	mount -o ro,loop $(RHUI_ISO) /mnt
	cd /mnt && ./install_CDS.sh && cd - && umount /mnt

.PHONY: fetch install-rhua install-cds

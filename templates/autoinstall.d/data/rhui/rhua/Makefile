# Makefile to fetch RHUI DVD iso image, install RHUI and generate certs.
# Requirements: openssl, curl or wget
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup
CERTSDIR = $(WORKDIR)/certs
QPID_SSL_VALID ?= 120

# @see http://red.ht/RAKEyc :
RHUI_CERT ?= $(WORKDIR)/$(notdir {{ rhui_entitlement_certs[0] }})
RHUI_ISO ?= RHEL-6-RHUI-2-LATEST-Server-x86_64-DVD.iso
RHUI_URL ?= https://cdn.redhat.com/content/dist/rhel/rhui/server/6/6Server/x86_64/rhui/2/iso/$(RHUI_ISO)

FETCH_PROG ?= curl

ifeq ($(FETCH_PROG),curl)
# TODO: curl doesn't look work well:
fetch_RHUI_ISO = curl --cert $(RHUI_CERT)
{% if proxy is defined and proxy.fqdn is defined -%}
fetch_RHUI_ISO += --proxy https://{{ proxy.fqdn }}:{{ proxy.port|default("443") }}
{%     if proxy.user is defined -%}
fetch_RHUI_ISO += --proxy-user {{ proxy.user }}:{{ proxy.password }}
{%-    endif %}
{%- endif %}
fetch_RHUI_ISO += -v --insecure -O
else
{% if proxy is defined and proxy.fqdn is defined -%}
fetch_RHUI_ISO = env https_proxy=https://{{ proxy.fqdn }}:{{ proxy.port|default("443") }} wget --certificate $(RHUI_CERT)
{%     if proxy.user is defined -%}
fetch_RHUI_ISO += --proxy-user={{ proxy.user }} --proxy-password={{ proxy.password }}
{%-    endif %}
{% else -%}
fetch_RHUI_ISO = wget --certificate $(RHUI_CERT)
{%- endif %}
fetch_RHUI_ISO += --no-check-certificate --secure-protocol=SSLv3
endif

CDS_CLUSTER ?= {{ cds.clusters }}

all:
	@echo "Usage: make [VAR_OVERRIDES ...]"
	@echo ""
	@echo "ex. make RHUI_URL=http://example.com/rhui.iso fetch_RHUI_ISO='curl ' fetch"
	@echo "ex. make install-rhua"
	@echo ""
	@echo "  Targets for RHUA: check fetch install-rhua certs genconf genkey"
	@echo ""

# common:
fetch: $(RHUI_ISO)
$(RHUI_ISO):
	$(fetch_RHUI_ISO) $(RHUI_URL)

check: $(WORKDIR)/check.stamp
$(WORKDIR)/check.stamp:
	date
	fqdn=`hostname -f`; test "x$$fqdn" = 'x{{ fqdn }}'
	touch $@

# On RHUA
install-rhua: $(WORKDIR)/install-rhua.stamp
$(WORKDIR)/install-rhua.stamp: $(RHUI_ISO)
	mount -o ro,loop $(RHUI_ISO) /mnt
	cd /mnt && ./install_RHUA.sh && cd - && umount /mnt
	touch $@

certs: $(CERTSDIR)/certs.stamp
$(CERTSDIR)/certs.stamp:
	test -f $@ || make -C $(CERTSDIR) certs

genconf: $(WORKDIR)/genconf.stamp
$(WORKDIR)/genconf.stamp: $(CERTSDIR)/certs.stamp $(WORKDIR)/answers.txt
	rhui-installer $(WORKDIR)/answers.txt 2>&1 | tee $(WORKDIR)/rhui-install.log

genkey: $(WORKDIR)/genkey.stamp
$(WORKDIR)/genkey.stamp: $(WORKDIR)/gen_rpm_gpgkey.sh
	bash -x $< 2>&1 | tee $<.log

.PHONY: check fetch install-rhua certs genconf genkey


#
# Makefile to install and do initial setup of RHUI v2.
#
# Author: Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# - Requirements: openssl, curl or wget
# - Overview of the steps (<> are Make targets):
#
#   0. [Optional] Register RHUA server to RH Portal site <register>
#   1. Collect some system info data and do some checks (access to RH CDN, etc.) <check>
#   2. Install RHUI RPMs and RHUI config RPM <install):
#
#      a. Install RHUI RPMs:
#
#         1) Download RHUI v2 Installation ISO image from RH CDN
#         2) Install RHUI v2 RPMs from the ISO image downloaded
#
#      b. Preparations before building RHUI Config RPMs:
#
#         - Generate SSL and Client Entitlement Certificates <certs>
#         - Generate and arrange a GPG Key Pair to sign RHUI Config RPMs later
#
#      c. Build RHUI Config RPMs <genconf>
#      d. Install RHUI Config RPM for RHUA <install-config-rpm>
#
#   3. Initial setup <setup>:
#
#      a. Install Client Entitlement Cert by run rhui-manager initially
#      b. Upload RHUI Entitlement Cert
#      c. Collect initial configuration of RHUI with using rhui-manager <init>
#
SHELL = bash  # To use some extensions.

WORKDIR ?= /root/setup
CERTSDIR = certs

# @see http://red.ht/RAKEyc :
RHUI_CERTS = $(wildcard *.pem)
RHUI_CERT ?= $(firstword $(RHUI_CERTS))
ifeq ($(strip $(RHUI_CERT)),)
$(error RHUI Entitlement Cert/Content Cert, *.pem was not found. Aborting...)
endif
RHUI_CERT_INSTALLED = /etc/pki/rhui/redhat/$(notdir $(RHUI_CERT))
RHUI_ISO ?= RHEL-6-RHUI-2-LATEST-Server-x86_64-DVD.iso
RHUI_ISO_URL = \
https://cdn.redhat.com/content/dist/rhel/rhui/server/6/6Server/x86_64/rhui/2/iso/$(RHUI_ISO)

CHECK_CDN_ACCESS ?= \
curl -v --cacert /etc/rhsm/ca/redhat-uep.pem --connect-timeout 5 https://cdn.redhat.com

DOWNLOAD_RHUI_ISO = curl -v --cacert /etc/rhsm/ca/redhat-uep.pem --cert ./$(RHUI_CERT) -O

# RPMs will be created and do not exist at first.
RHUA_CONFIG_RPM_NAME ?= rh-rhua-config
RHUA_CONFIG_RPM ?= $(firstword $(wildcard rhui/$(RHUA_CONFIG_RPM_NAME)-*.rpm))
RHUI_CONFIG_RPMS ?= $(wildcard rhui/rh-*-config-*.rpm)

RHUI_GPG_PUB_KEY ?= RPM-GPG-KEY-rhui-custom
RHUI_GPG_PUB_KEY_INSTALLED = /etc/pki/rpm-gpg/$(RHUI_GPG_PUB_KEY)

RHUI_CLIENT_ENTITLEMENT_CA_CERT ?= /etc/pki/rhui/entitlement-ca.crt
RHUI_CLIENT_ENTITLEMENT_CA_FILES ?= \
$(RHUI_CLIENT_ENTITLEMENT_CA_CERT) \
/etc/pki/rhui/entitlement-ca-key.pem
#/etc/pki/rhui/entitlement-ca.srl

RHUI_CLIENT_ENTITLEMENT_CA_SRCS = \
$(subst /etc/pki/rhui,certs,$(RHUI_CLIENT_ENTITLEMENT_CA_FILES))
SHOW_RHUI_MANAGER_HELP_TEXTS ?= collect_rhui-manager_help_recur.sh

IS_RHUI_INSTALLED = rpm -q rh-rhui-tools

-include Makefile.vars


all:
	@echo "Usage: make [VAR_OVERRIDES ...]"
	@echo ""
	@echo "Examples:"
	@echo "  make check"
	@echo "  make RHUI_ISO_URL=http://example.com/rhui.iso install"
	@echo ""
	@echo "  Targets: [register] check install [certs genconf] init"
	@echo ""

# common:
register:
	subscription-manager unregister || :
	subscription-manager clean || :
	subscription-manager register --type=rhui $(SUBSCRIPTION_MANAGER_OPTIONS)
	subscription-manager repos --disable '*'
	subscription-manager repos --enable rhel-6-server-rhui-rpms --enable rhel-x86_64-6-rhui-2-rpms
	@echo "Now you ready to generate RHUI entitlement cert on: https://access.redhat.com/management/consumers/ "

check: check.stamp
check.stamp:
	date
	fqdn=`hostname -f`; test "x$$fqdn" = 'x{{ fqdn }}'
	rpm -q ntp && service ntpd status && which ntptime && ntptime || :
	test -f check.sh && bash -x ./check.sh || :
	$(CHECK_CDN_ACCESS)
	touch $@

$(RHUI_ISO):
	$(DOWNLOAD_RHUI_ISO) $(RHUI_ISO_URL)

install-rhui-rpms.stamp: $(RHUI_ISO)
	$(IS_RHUI_INSTALLED) || \
	mount -o ro,loop $(RHUI_ISO) /mnt && cd /mnt && ./install_RHUA.sh && cd - && umount /mnt
	touch $@

certs: $(CERTSDIR)/certs.stamp
$(CERTSDIR)/certs.stamp:
	test -f $@ || make -C $(CERTSDIR)

# TODO:
#$(CERTSDIR)/certs.stamp:
#	/usr/share/rh-rhua/rhui_certs/create_rhui_ssl_certs.sh \
#		--country {{ rhui.ssl.country|default('JP') }} \
#		--state {{ rhui.ssl.state|default('Tokyo') }} \
#		$(shell hostname) {{ cdsservers|join(' ', attribute='fqdn') }}

# FIXME: Remove the file check.
genconf: genconf.stamp
genconf.stamp: install-rhui-rpms.stamp $(CERTSDIR)/certs.stamp answers.txt
	test -f $@ || rhui-installer answers.txt 2>&1 | tee rhui-install.log
	touch $@

$(RHUI_GPG_PUB_KEY): gen_rpm_gpgkey.sh
	bash -x $< 2>&1 | tee $<.log

$(RHUI_GPG_PUB_KEY_INSTALLED): $(RHUI_GPG_PUB_KEY)
	install -m 644 $< $(dir $@)

.PHONY: register check install certs genconf

install: install-config-rpm.stamp
install-config-rpm.stamp: genconf.stamp $(RHUI_GPG_PUB_KEY_INSTALLED)
	rpm -Kv $(RHUI_CONFIG_RPMS) | grep Signature > /dev/null || rpm --resign $(RHUI_CONFIG_RPMS)
	rpm -Kv $(RHUI_CONFIG_RPMS) | grep -E 'Signature .* OK' > /dev/null || rpm --import $(RHUI_GPG_PUB_KEY_INSTALLED)
	rpm -q $(RHUA_CONFIG_RPM_NAME) || \
	(rpm -qi `rpm -qa gpg-pubkey*` && \
	rpm -Kv $(RHUI_CONFIG_RPMS) && \
	for p in $(RHUI_CONFIG_RPMS); do echo "# $$p"; rpm -qlp $$p; rpm -qp --scripts $$p; done && \
	yum install -y $(RHUA_CONFIG_RPM) && \
	service pulp-server status)
	touch $@


# FIXME: Remove the file check.
$(RHUI_CLIENT_ENTITLEMENT_CA_FILES): install-config-rpm.stamp
	test -f $(RHUI_CLIENT_ENTITLEMENT_CA_CERT) || rhui-manager

$(RHUI_CERT_INSTALLED): $(RHUI_CERT) $(RHUI_CLIENT_ENTITLEMENT_CA_FILES)
	echo -ne "n\nl\nq\n" | rhui-manager; echo
	rhui-manager --help
	rhui-manager cert --help
	rhui-manager cert upload --help
	rhui-manager cert upload --cert $<
	rhui-manager cert info

init: init.stamp
init.stamp: $(RHUI_CERT_INSTALLED)
	cs=''; for c in r c n; do cs="$$cs<\n$$c\nl\n"; done; \
	for c in s e u i; do cs="$$cs<\n$$c\n"; done; \
	cs=$$cs"q\n"; echo -ne "$$cs" | rhui-manager; echo
	bash -x $(SHOW_RHUI_MANAGER_HELP_TEXTS)
	rhui-manager client labels | sort
	rhui-manager status

.PHONY: install init setup

build-client-config-rpms.stamp: init.stamp
	test -f $@ || $(BUILD_CLIENT_CONFIG_RPMS)
	touch $@



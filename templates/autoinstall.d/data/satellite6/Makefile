# Makefile to install and setup Satellite-6.
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
# Overview of the steps:
#   1. Checks
#   2. Installation
#   3. Setup
#   4. Sync
#   5. Promote & Publish
#
# References:
#   - Satellite 6.1 beta Installation Guide
#   - Red Hat Satellite 6.1 Beta Guide: https://access.redhat.com/articles/1380023
#

# Load variables, etc.
-include Makefile.custom

# 1. Checks:
CHECK_IF_NTPD_IS_SYNCHED ?= $(CHECK_IF_NTPD_IS_RUNNING_AND_ENABLED) && ntptime
CHECK_CLOCK ?= date && $(CHECK_IF_NTPD_IS_SYNCHED)

CHECK_FQND ?= \
hostname && hostname -f && hostname -s && \
ping -c1 -w3 localhost && ping -c1 -w3 `hostname -s` && \
ping -c1 -w3 `hostname -f`

CHECK_CDN_ACCESS ?= \
curl -vk --connect-timeout 5 $(CURL_PROXY_OPT) https://cdn.redhat.com

# 2. Installation:
#   a. Install Satellite RPMs from ISO image or RHN
#   b. Do configuration necessary for satellite installation 
#   c. Install Satellite w/ its installer, katello-installer
#
# References: Satellite 6.1 beta Installation Guide,
#   - 1.4. Prerequisites: http://red.ht/1Hki76R
#   - 2.1.2. Downloading from a Disconnected Network: http://red.ht/1MlR1jf
#   - 2.2. Running the Installation and Configuration Program: http://red.ht/1NVBbMD

# a-1. Offline installation w/ ISO image downloaded before.
SETUP_SATELLITE_ISO ?= \
cd $(WORKDIR) && (test -f satellite.iso || ln -sf `ls -1 satellite*.iso | head -n 1` satellite.iso)

INSTALL_SATELLITE_RPMS_FROM_ISO = \
test -f $(SATELLITE_ISO) && \
trap "umount /mnt" INT TERM && \
mount -o ro,loop $(SATELLITE_ISO) /mnt && \
cd /mnt && ./install_packages && cd - && umount /mnt

# a-2. Online installation from RHN.
INSTALL_SATELLITE_RPMS_FROM_RHN = yum install -y katello

# Make offline installation default for safety.
INSTALL_SATELLITE_RPMS = \
rpm -q katello || ($(INSTALL_SATELLITE_RPMS_FROM_ISO))

# b. Configuraiton:
# It seems the problme w/ openjdk 1.8 was fixed, rhbz#1216180
# (https://bugzilla.redhat.com/show_bug.cgi?id=1216180) thus, this hack is not
# needed anymore, I guess.
#CONFIGURE_JAVA = \
#alternatives --set java `echo /usr/lib/jvm/java-1.7.0-openjdk-*/jre/bin/java` || :
# Instead, ensure that openjdk 1.8 is used.
CONFIGURE_JAVA = \
alternatives --set java `echo /usr/lib/jvm/java-1.8.*-openjdk-*/jre/bin/java` || :

CONFIGURE_BEFORE_SATELLITE_INSTALLATION = \
$(CONFIGURE_JAVA)

# c.
INSTALL_SATELLITE = \
katello-installer $(KATELLO_INSTALLER_OPTIONS) 2>&1 | tee $(LOGDIR)/katello-installer.log

# 3. Setup:
#   a. Setup hammer user conf
#   b. Create Organization and Location
#   c. Load Manifest
#   d. Enable desired repositories for access.redhat.com
#   Create CDN: Sync Plan and sync content.
#   Create lifecycle environment path(s).
#   Create a RHEL X.Y Content View.
#   Create an activation key that provides subscriptions for these Products.
#   Publish and promote 1 or more CVs.
#
SETUP_HAMMER_USER_CONF = \
test -f $(HAMMER_USER_CONF) || \
(test -d $(dir HAMMER_USER_CONF) || \
 mkdir -m 0700 $(dir HAMMER_USER_CONF); \
 cp $(HAMMER_SYS_CONF) $(HAMMER_USER_CONF) && \
 chmod 600 $(HAMMER_USER_CONF) && \
 echo "" >> $(HAMMER_USER_CONF) && \
 echo "  :username: $(HAMMER_ADMIN_NAME)" >> $(HAMMER_USER_CONF) && \
 echo "  :password: $(HAMMER_ADMIN_PASSWORD)" >> $(HAMMER_USER_CONF))

ORGID_FILE = $(LOGDIR)/orgid.txt

SETUP_ORG = \
org_id=`hammer organization list | sed -nr "s/^([[:digit:]]+) .*$(ORG_NAME).*/\1/p"`; \
(test "x$${org_id}" = "x" && \
 hammer organization create --name="$(ORG_NAME)" --label="$(ORG_LABEL)" || :) && \
hammer organization add-user --name="$(ORG_NAME)" --user="$(ADMIN_NAME)" && \
org_id=`hammer organization list | sed -nr "s/^([[:digit:]]+) .*$(ORG_NAME).*/\1/p"`; \
test "x$${org_id}" != "x" && echo $${org_id} > $(ORGID_FILE)

SETUP_LOCATION = \
loc_id=`hammer location list | sed -nr "s/^([[:digit:]]+) .*$(LOCATION_NAME).*/\1/p"`; \
(test "x$${loc_id}" = "x" && hammer location create --name="$(LOCATION_NAME)" || :); \
hammer location add-user --name="$(LOCATION_NAME)" --user="$(ADMIN_NAME)"; \
hammer location add-organization --name="$(LOCATION_NAME)" --organization="$(ORG_NAME)"


LOAD_MANIFEST = \
(test -f $(MANIFETS_FILE).base64 -a ! -f $(MANIFETS_FILE) && \
 base64 -d $(MANIFETS_FILE).base64 > $(MANIFETS_FILE) || :); \
hammer subscription upload --organization-id `cat $(ORGID_FILE)` --file $(MANIFET_FILE)

SETUP_DAILY_SYNC_PLAN = \
hammer sync-plan create --organization "$(ORG_NAME)" --interval daily --name "Daily Sync" --enabled false && \
hammer product set-sync-plan --organization-id `cat $(ORGID_FILE)` \
  --name "$(PRODUCT)" --sync-plan-id 1  # It seems that --sync-plan is not valid.

#SYNC_REPOS = \
#PUBLISH_AND_PROMOTE_CONTENT_VIEWS = \


all:
	@echo "Usage: make (check | install | setup | sync | publish)"


$(LOGDIR):
	mkdir -p $(LOGDIR)

check: check.stamp
check.stamp: $(LOGDIR)
	$(CHECK_CLOCK)
	$(CHECK_FQDN)
	$(CHECK_CDN_ACCESS)
	touch $@

install: install.stamp
install.stamp: check.stamp $(SATELLITE_ISO)
	$(SETUP_SATELLITE_ISO)
	$(INSTALL_SATELLITE_RPMS)
	$(CONFIGURE_BEFORE_SATELLITE_INSTALLATION)
	$(INSTALL_SATELLITE)
	touch $@

setup: setup.stamp
setup.stamp: install.stamp
	$(SETUP_HAMMER_USER_CONF)
	$(SETUP_ORG)
	$(SETUP_LOCATION)
	$(LOAD_MANIFEST)
	$(SETUP_REPOS)
	$(SETUP_DAILY_SYNC_PLAN)
	$(SETUP_LIFECYCLE_ENV_PATHS)
	$(SETUP_CONTENT_VIEWS)
	$(SETUP_HOST_COLLECTIONS)

sync:
	@echo TBD

publish:
	@echo TBD
	exit 1
	$(SETUP_ACTIVATION_KEYS)


.PHONY: check install setup sync publish
# vim:noet:

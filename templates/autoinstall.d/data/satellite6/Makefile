# Makefile to install and setup Satellite-6.
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
# Overview of the steps:
#   0. Checks:
#      a. Check FQDN: hostname -f
#      b. Check date and time: date, ntptime, etc.
#
#   1. Installation:
#      a. Satellite RPM Installation: ./install_packages in Satellite ISO image
#      b. Satellite Installation: katello-installer
#
#   2. Setup:
#      a. Setup hammer user configuration and check access: cat ... & hammer ping
#      b. Setup Organization [option; if default organization is not used]: hammer organization create
#      c. Setup Location [option; if default location is not used]: hammer location create
#      d. Upload Satellite manifest: hammer subscription upload
#      e. Setup Lifecycle Environments: hammer lifecycle-environment create
#      f. Setup Yum Repos: hammer repository-set enable
#      g. Setup Sync Plan:
#         - online: hammer sync-plan create --enabled true
#         - offline: hammer sync-plan create --enabled false
#
#      h. Setup Host Collection: hammer host-collection create
#      i. Setup Content View [option]: hammer content-view create, hammer content-view add-repository
#      j. Setup Activation Keys: hammer activation-key create
#      k. Setup Users [option]:
#         - setup LDAP or other auth sources [option]: ex. hammer auth-source ldap create ...
#         - create a user: hammer user create
#
#   3. Sync:
#      a. Check access to CDN: curl https://cdn.redhat.com
#      b. Sync Yum Repos: hammer repository synchronize
#      c. Enable Sync Plan [option: if offline -> online]: hammer sync-plan update --enabled true
#
#   4. Publish & Promote:
#      a. Publish Content Views [option]: hammer content-view publish
#      b. Promote Content Views [option]: hammer content-view version promote
#
#   5. Test clients:
#      a. [client]: Install Satellite SSL CA RPM: yum install -y
#      b. [client]: Register: subscription-manager register
#      c. [satellite]: Check registration of content host: hammer content-host list
#      d. [client]: Test access to Satellite: yum repolist, yum updateinfo list, etc.
#
# References:
#   - https://access.redhat.com/documentation/en/red-hat-satellite/
#   - https://github.com/Katello/hammer-cli-katello/tree/master/lib/hammer_cli_katello
#   - https://access.redhat.com/solutions/1607873
#   - https://access.redhat.com/solutions/1229603
#
WORKDIR ?= /root/setup
LOGDIR ?= $(WORKDIR)/logs
SATELLITE_ISO_DIR ?= $(WORKDIR)

# Defaults if not set in the above Makefile:
SATELLITE_HOSTNAME ?= $(shell hostname)
TIMESTAMP = $(shell date +%F_%T)

# Options for katello-installer. Customize this as needed.
# ex. KATELLO_INSTALLER_OPTIONS ?= --verbose --foreman-admin-email=foo@example.com --proxy-url ...
#
KATELLO_INSTALLER_OPTIONS ?= --verbose

PROXY_URL ?=
CURL_PROXY_OPT ?=

ADMIN_NAME = admin
ORG_NAME ?= Default Organization
ORG_LABEL ?= Default_Organization
LOCATION_NAME ?= Default Location

LIFECYCLE_ENV_PATHS ?= Test Prod
HOST_COLLECTIONS ?= HC_RHEL_7 HC_RHEL_6
SYNC_PLAN_NAME ?= Daily Sync

CLIENT_YUM_REPO_0 ?= \
--basearch x86_64 --product 'Red Hat Enterprise Linux Server' \
--name 'Red Hat Enterprise Linux 7 Server (RPMs)' --releasever 7Server

CLIENT_YUM_REPO_1 ?= \
--basearch x86_64 --product 'Red Hat Enterprise Linux Server' \
--name 'Red Hat Enterprise Linux 7 Server - Optional (RPMs)' --releasever 7Server

CLIENT_YUM_REPO_3 ?= \
--basearch x86_64 --product 'Red Hat Software Collections for RHEL Server' \
--name 'Red Hat Software Collections RPMs For Red Hat Enterprise Linux 7 Server'

CLIENT_YUM_REPO_4 ?= \
--basearch x86_64 --product 'Red Hat Satellite' \
--name 'Red Hat Satellite 6.1 (For RHEL 7 Server) (RPMs)'

CLIENT_YUM_REPO_5 ?= \
--basearch x86_64 --product 'Red Hat Enterprise Linux Server' \
--name 'Red Hat Satellite Tools 6.1 (For RHEL 7 Server) (RPMs)'

#CLIENT_YUM_REPO_6 ?= \
#--basearch x86_64 --product 'Red Hat Enterprise Linux Server' \
#--name 'Red Hat Enterprise Linux 6 Server (RPMs)' --releasever 6Server
#
#CLIENT_YUM_REPO_7 ?= \
#-basearch x86_64 --product 'Red Hat Enterprise Linux Server' \
#--name 'Red Hat Enterprise Linux 6 Server - Optional (RPMs)' --releasever 6Server
#
#CLIENT_YUM_REPO_8 ?= \
#--basearch x86_64 --product 'Red Hat Enterprise Linux Server' \
#--name 'Red Hat Satellite Tools 6.1 (For RHEL 6 Server) (RPMs)'

SATELLITE_ACTIVATION_KEY ?= key_HC_RHEL_7
SATELLITE_ORG ?= $(ORG_LABEL)

# Load variables, etc.
-include Makefile.custom


## main:
all:
	@echo "Usage: make (check | install | setup | register-self | sync)"

# 0. Checks:
#    a. Check FQDN: hostname -f
#    b. Check date and time: date, ntptime, etc.
#
# TODO: How to check the clock if chrony is used ?
#
CHECK_CDN_ACCESS ?= \
curl -v --cacet /etc/rhsm/ca/redhat-uep.pem --connect-timeout 5 \
$(CURL_PROXY_OPT) https://cdn.redhat.com

CHECK_FQDN ?= \
(hostname && hostname -f && hostname -s && \
ping -c1 -w3 localhost && ping -c1 -w3 `hostname -s` && \
ping -c1 -w3 `hostname -f`)

CHECK_DATETIME = (date && \
rpm -q chrony 2>/dev/null && \
(systemctl status chronyd && systemctl is-enabled chronyd && chronyc sources) || \
(rpm -q ntp 2>/dev/null && systemctl status ntpd && systemctl is-enabled ntpd && ntptime))

$(LOGDIR):
	mkdir -p $@

check: check.stamp
check.stamp: $(LOGDIR)
	bash -x check.sh
	$(CHECK_CDN_ACCESS) | tee $(LOGDIR).check.cdn_access.$(TIMESTAMP).log
	$(CHECK_FQDN) | tee $(LOGDIR).check.fqdn.$(TIMESTAMP).log
	$(CHECK_DATETIME) | tee $(LOGDIR).check.datetime.$(TIMESTAMP).log
	touch $@

.PHONY: check

# 1. Installation:
#    a. Satellite RPM Installation: ./install_packages in Satellite ISO image
#    b. Satellite Installation: katello-installer
#
# References: Satellite 6.1 Installation Guide,
#   - 1.4. Prerequisites: http://red.ht/1Hki76R
#   - 2.1.2. Downloading from a Disconnected Network: http://red.ht/1MlR1jf
#   - 2.2. Running the Installation and Configuration Program: http://red.ht/1NVBbMD
#
SATELLITE_ISO ?= $(strip $(shell ls -1 $(SATELLITE_ISO_DIR)/satellite*.iso | head -n 1))
ifeq ($(SATELLITE_ISO),)
$(error Satellite ISO image is missing!)
endif

INSTALL_SATELLITE_RPMS_FROM_ISO = \
test -f $(SATELLITE_ISO) && trap "umount /mnt" INT TERM && \
mount -o ro,loop $(SATELLITE_ISO) /mnt && cd /mnt && ./install_packages; \
cd - && umount /mnt

install: install.stamp
install.stamp: $(LOGDIR)
	rpm -q katello || $(INSTALL_SATELLITE_RPMS_FROM_ISO)
	katello-installer $(KATELLO_INSTALLER_OPTIONS) 2>&1 | \
		tee $(LOGDIR)/katello-installer.$(TIMESTAMP).log)
	touch $@

.PHONY: install

# 2. Setup:
#    a. Setup hammer user configuration and check access: cat ... & hammer ping
#
HAMMER_SYS_CONF ?= /etc/hammer/cli.modules.d/foreman.yml
HAMMER_USER_CONF ?= ~/.hammer/cli_config.yml
HAMMER_USER_CONF_DIR ?= $(dir $(HAMMER_USER_CONF))

HAMMER_ADMIN_NAME ?= $(ADMIN_NAME)
# http://gsw-hammer.documentation.rocks/initial_configuration,_adding_red_repos/hammer_credentials.html
HAMMER_ADMIN_PASSWORD ?= \
$(shell sed -nr 's/^ *admin_password: ([^[:blank:]]+) *$$/\1/p' \
  /etc/katello-installer/answers.katello-installer.yaml)

$(HAMMER_USER_CONF_DIR):
	mkdir -p -m 0700 $@

$(HAMMER_USER_CONF): $(HAMMER_SYS_CONF) $(HAMMER_USER_CONF_DIR)
	install -m 600 $(HAMMER_SYS_CONF) $(HAMMER_USER_CONF)
	echo "" >> $(HAMMER_USER_CONF) && \
	echo '  :username: $(HAMMER_ADMIN_NAME)' >> $(HAMMER_USER_CONF) && \
	echo '  :password: $(HAMMER_ADMIN_PASSWORD)' >> $(HAMMER_USER_CONF) && \
	echo "" >> $(HAMMER_USER_CONF)

# b. Setup Organization [option; if default organization is not used]:
#    hammer organization create
#
ORG_ID_FILE ?= ~/.hammer/organization_id.txt

$(ORG_ID_FILE): $(HAMMER_USER_CONF)
	hammer --csv organization list | grep -qE ',$(ORG_LABEL),$$' 2>/dev/null || \
	hammer organization create --name='$(ORG_NAME)' --label='$(ORG_LABEL)'
	hammer --output=yaml organization info --label '$(ORG_LABEL)' | sed -nr "s/^Id: //p" > $@.t
	test -s $@.t && mv $@.t $@

setup-organization: $(ORG_ID_FILE)

.PHONY: setup-organization

# c. Setup Location [option; if default location is not used]:
#    hammer location create
#
LOC_ID_FILE ?= ~/.hammer/location_id.txt

$(LOC_ID_FILE):
	hammer --csv location list | grep -qE ',$(LOCATION_NAME)$$' 2>/dev/null || \
	hammer location create --name '$(LOCATION_NAME)'
	hammer --output=yaml location info --name '$(LOCATION_NAME)' | sed -nr "s/^Id: //p" > $@.t
	test -s $@.t && mv $@.t $@

setup-location: $(LOC_ID_FILE)

.PHONY: setup-location

# d. Upload Satellite manifest: hammer subscription upload
# - manifest.zip may be base64-encoded.
#
MANIFEST_ZIP_BASE64 = $(strip $(firstword $(wildcard manifest*.zip.base64)))
ifneq ($(MANIFEST_ZIP_BASE64),)
MANIFEST_ZIP = $(MANIFEST_ZIP_BASE64:.base64=)
$(MANIFEST_ZIP): $(MANIFEST_ZIP_BASE64)
	base64 -d $< > $@
else
MANIFEST_ZIP ?= $(strip $(firstword $(wildcard manifest*.zip)))
endif

ifeq ($(MANIFEST_ZIP),)
$(error Neither Manifest zip file nor its base64 encoded version are missing!)
endif

upload-manifest: upload-manifest.stamp
upload-manifest.stamp: $(MANIFEST_ZIP) $(ORG_ID_FILE)
	hammer subscription upload --organization-id `cat $(ORG_ID_FILE)` --file $(MANIFEST_ZIP)
	touch $@

.PHONY: upload-manifest

# e. Setup Lifecycle Environments: hammer lifecycle-environment create
#
setup-lifecycle-environments: $(ORG_ID_FILE)
	les=$$(hammer --csv lifecycle-environment list --organization-id `cat $(ORG_ID_FILE)`); \
	prev_le=Library; \
	for cur_le in $(LIFECYCLE_ENV_PATHS); do \
		echo "$$les" | grep -qE ",$$cur_le," || \
		hammer lifecycle-environment create --organization-id `cat $(ORG_ID_FILE)` \
			--prior "$$prev_le" --name "$$cur_le"; \
		prev_le=$$cur_le; \
	done

.PHONY: setup-lifecycle-environments

# f. Setup Yum Repos: hammer repository-set enable
#
HAMMER_ENABLE_REPO = hammer repository-set enable --organization-id `cat $(ORG_ID_FILE)` 
setup-yum-repos: $(ORG_ID_FILE)
	test -z "$(CLIENT_YUM_REPO_0)" || $(HAMMER_ENABLE_REPO) $(CLIENT_YUM_REPO_0)
	test -z "$(CLIENT_YUM_REPO_1)" || $(HAMMER_ENABLE_REPO) $(CLIENT_YUM_REPO_1)
	test -z "$(CLIENT_YUM_REPO_2)" || $(HAMMER_ENABLE_REPO) $(CLIENT_YUM_REPO_2)
	test -z "$(CLIENT_YUM_REPO_3)" || $(HAMMER_ENABLE_REPO) $(CLIENT_YUM_REPO_3)
	test -z "$(CLIENT_YUM_REPO_4)" || $(HAMMER_ENABLE_REPO) $(CLIENT_YUM_REPO_4)
	test -z "$(CLIENT_YUM_REPO_5)" || $(HAMMER_ENABLE_REPO) $(CLIENT_YUM_REPO_5)

.PHONY: setup-yum-repos

# g. Setup Sync Plan:
#    - online: hammer sync-plan create --enabled true
#    - offline: hammer sync-plan create --enabled false
#
# Note: --sync-plan does not looks valid option for hammer product set-sync-plan.
#
setup-sync-plan: $(ORG_ID_FILE)
	spid=$$(hammer --output=yaml sync-plan list --organization-id `cat $(ORG_ID_FILE)` \
		--name '$(SYNC_PLAN_NAME)' | sed -nr 's/.*ID: //p'); \
	if test "x$$spid" = "x"; then \
	hammer sync-plan create --organization-id `cat $(ORG_ID_FILE)` \
		--interval daily --name '$(SYNC_PLAN_NAME)' --enabled false; \
	hammer product set-sync-plan --organization-id `cat $(ORG_ID_FILE)` \
	  --name 'Red Hat Enterprise Linux Server' --sync-plan-id 1 && \
	hammer product set-sync-plan --organization-id `cat $(ORG_ID_FILE)` \
	  --name 'Red Hat Satellite' --sync-plan-id 1 && \
	hammer product set-sync-plan --organization-id `cat $(ORG_ID_FILE)` \
	  --name 'Red Hat Software Collections for RHEL Server' --sync-plan-id 1; \
	fi

.PHONY: setup-sync-plan

# h. Setup Host Collection: hammer host-collection create
#
setup-host-collections: $(ORG_ID_FILE)
	hcs=$$(hammer --csv host-collection list --organization-id `cat $(ORG_ID_FILE)`); \
	for hc in $(HOST_COLLECTIONS); do \
		echo "$$hcs" | grep -qE ",$$hc," || \
		hammer host-collection create --organization-id `cat $(ORG_ID_FILE)` --name "$$hc"; \
	done

.PHONY: setup-host-collections

# i. Setup Content View [option]:
#    hammer content-view create, hammer content-view add-repository
#
# TODO:
SETUP_CONTENT_VIEWS ?= :


# j. Setup Activation Keys: hammer activation-key create
#
# TODO:
# - fix names of activation keys
# - add subscriptions:
#   hammer activation-key add-subscription --organization "<organization_name>" 
#     --name <key_name> --subscription-id <subscription_id> --quantity <quantity>
#
setup-activation-keys: $(ORG_ID_FILE)
	aks=$$(hammer --csv activation-key list --organization-id `cat $(ORG_ID_FILE)`); \
	for hc in $(HOST_COLLECTIONS); do \
		akey=key_$$hc; \
		echo "$$aks" | grep -qE ",$$akey," 2>/devnull || \
		(hammer activation-key create --organization-id `cat $(ORG_ID_FILE)` \
			--name "$$akey" --content-view 'Default Organization View' \
			--lifecycle-environment 'Library' --unlimited-content-hosts true && \
		hammer activation-key add-host-collection --organization-id `cat $(ORG_ID_FILE)` \
			--host-collection "$$hc" --name "$$akey"); \
	done

.PHONY: setup-activation-keys

# 5. Test clients:
#    a. [client]: Install Satellite SSL CA RPM: yum install -y
#    b. [client]: Register: subscription-manager register
#    c. [satellite]: Check registration of content host: hammer content-host list
#    d. [client]: Test access to Satellite: yum repolist, yum updateinfo list, etc.
#
register-self: register-self.stamp
register-self.stamp:
	rpm -q katello-ca-consumer-$(SATELLITE_HOSTNAME) || \
	yum install -y /var/www/html/pub/katello-ca-consumer-latest.noarch.rpm
	subscription-manager identity || \
	(subscription-manager register --activationkey $(SATELLITE_ACTIVATION_KEY) \
		--org="$(SATELLITE_ORG)" && subscription-manager identity)
	hammer --csv content-host list --organization-id `cat $(ORG_ID_FILE)` --search $(SATELLITE_HOSTNAME)
	touch $@

.PHONY: register-self

# main:
setup-all: setup-organization
setup-all: setup-location
setup-all: upload-manifest
setup-all: setup-lifecycle-environments
setup-all: setup-sync-plan
setup-all: setup-host-collections
setup-all: setup-activation-keys

# Require access to cdn.redhat.com:
setup-all: setup-yum-repos

setup: setup-all

.PHONY: setup setup-all

# Yum Repository synchronization by manual
SYNC_REPOS_BY_PRODUCT = hammer product synchronize --organization-id `cat $(ORGID_FILE)` --async
SYNC_REPOS_BY_REPO = hammer repository synchronize --organization "$(ORG_NAME)" --async

sync-by-product: sync-by-product.stamp
sync-by-product.stamp:
	$(SYNC_REPOS_BY_PRODUCT) --name "Red Hat Enterprise Linux Server" || :
	$(SYNC_REPOS_BY_PRODUCT) --name "Red Hat Satellite" || :
	$(SYNC_REPOS_BY_PRODUCT) --name "Red Hat Software Collections for RHEL Server" || :
	touch $@

sync-by-reop: sync-by-reop.stamp
sync-by-reop.stamp:
	$(SYNC_REPOS_BY_REPO) $(CLIENT_YUM_REPO_0) || :
	$(SYNC_REPOS_BY_REPO) $(CLIENT_YUM_REPO_1) || :
	$(SYNC_REPOS_BY_REPO) $(CLIENT_YUM_REPO_2) || :
	$(SYNC_REPOS_BY_REPO) $(CLIENT_YUM_REPO_3) || :
	$(SYNC_REPOS_BY_REPO) $(CLIENT_YUM_REPO_4) || :
	$(SYNC_REPOS_BY_REPO) $(CLIENT_YUM_REPO_5) || :
	touch $@

.PHONY: sync-by-product sync-by-repo

sync: sync-by-product # sync-by-repo

# vim:noet:ft=make:

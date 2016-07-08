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
#   - Red Hat Satellite 6.1 Guide: https://access.redhat.com/articles/1380023
#   - https://github.com/Katello/hammer-cli-katello/tree/master/lib/hammer_cli_katello
#   - https://access.redhat.com/solutions/1607873
#   - https://access.redhat.com/solutions/1229603
#

# Load variables, etc.
-include Makefile.custom

# 1. Checks:
CHECK_IF_NTPD_IS_SYNCHED ?= $(CHECK_IF_NTPD_IS_RUNNING_AND_ENABLED) && ntptime
CHECK_CLOCK ?= date && $(CHECK_IF_NTPD_IS_SYNCHED)

CHECK_FQDN ?= \
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
# References: Satellite 6.1 Installation Guide,
#   - 1.4. Prerequisites: http://red.ht/1Hki76R
#   - 2.1.2. Downloading from a Disconnected Network: http://red.ht/1MlR1jf
#   - 2.2. Running the Installation and Configuration Program: http://red.ht/1NVBbMD

# Yum repos (software collection) are required anyway:
SETUP_RHN ?= \
subscription-manager identity || \
subscription-manager register $(SUBSCRIPTION_MANAGER_REGISTER_OPTS) && \
subscription-manager repos --disable '*' && \
test -f /etc/systemd && \
subscription-manager repos \
    --enable rhel-7-server-rpms \
    --enable rhel-server-rhscl-7-rpms \
    --enable rhel-server-7-satellite-6-rpms || \
subscription-manager repos \
    --enable rhel-6-server-rpms \
    --enable rhel-server-rhscl-6-rpms \
    --enable rhel-server-6-satellite-6-rpms

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
(test -d $(dir $(HAMMER_USER_CONF)) || \
 mkdir -m 0700 $(dir $(HAMMER_USER_CONF)); \
 cp $(HAMMER_SYS_CONF) $(HAMMER_USER_CONF) && \
 chmod 600 $(HAMMER_USER_CONF) && \
 echo "" >> $(HAMMER_USER_CONF) && \
 echo "  :username: $(HAMMER_ADMIN_NAME)" >> $(HAMMER_USER_CONF) && \
 echo "  :password: $(HAMMER_ADMIN_PASSWORD)" >> $(HAMMER_USER_CONF))

ORGID_FILE = $(LOGDIR)/orgid.txt

SETUP_ORG = \
(hammer --csv organization list | grep -E '^[[:digit:]]+,$(ORG_NAME),.+') || \
hammer organization create --name="$(ORG_NAME)" --label="$(ORG_LABEL)"; \
hammer --output yaml organization info --name="$(ORG_NAME)" | grep -E 'login: $(ADMIN_NAME)$$' || \
hammer organization add-user --name="$(ORG_NAME)" --user="$(ADMIN_NAME)"; \
org_id=`hammer --csv organization list | sed -nr 's/^([[:digit:]]+),$(ORG_NAME),.+/\1/p'`; \
test "x$${org_id}" != "x" && echo $${org_id} > $(ORGID_FILE)

SETUP_LOCATION = \
(hammer --csv location list | grep -E '^[[:digit:]]+,$(LOCATION_NAME)') || \
hammer location create --name="$(LOCATION_NAME)"; \
loc_info=`hammer --output yaml location info --name="$(LOCATION_NAME)"` && \
(echo $$loc_info | grep -E 'login: $(ADMIN_NAME)$$' 2>/dev/null) || \
hammer location add-user --name="$(LOCATION_NAME)" --user="$(ADMIN_NAME)"; \
(echo $$loc_info | grep -E 'name: $(ORG_NAME)$$' 2>/dev/null) || \
hammer location add-organization --name="$(LOCATION_NAME)" --organization "$(ORG_NAME)"

LOAD_MANIFEST = \
cd $(WORKDIR) && \
(manifest_base64=`ls -1 manifest*.base64 | head -n 1`; \
 test "x$$manifest_base64" != "x" && test ! -f $(MANIFEST_FILE).base64 && \
 ln -sf $$manifest_base64 $(MANIFEST_FILE).base64); \
test -f $(MANIFEST_FILE).base64 -a ! -f $(MANIFEST_FILE) && \
base64 -d $(MANIFEST_FILE).base64 > $(MANIFEST_FILE) || :; \
hammer subscription upload --organization "$(ORG_NAME)" --file $(MANIFEST_FILE)

SETUP_DAILY_SYNC_PLAN = \
hammer sync-plan create --organization "$(ORG_NAME)" \
  --interval daily --name "Daily Sync" --enabled true && \
hammer product set-sync-plan --organization-id `cat $(ORGID_FILE)` \
  --name "$(PRODUCT)" --sync-plan-id 1  # It seems that --sync-plan is not valid.

SYNC_REPOS_BY_PRODUCT = \
hammer product synchronize --name "$(PRODUCT)" --organization-id `cat $(ORGID_FILE)`

SYNC_REPOS = \
for rid in \
    `hammer --output yaml repository list --organization "$(ORG_NAME)" | \
     sed -nr 's/.*Id: ([[:digit:]]+)/\1/p'`; do \
    hammer repository synchronize --organization "$(ORG_NAME)" --id $$rid --async; \
done

PUBLISH_REPOS = \
for cid in \
    `hammer --output yaml content-view list --organization "$(ORG_NAME)" --nondefault 1 | \
     sed -nr 's/.*Content View ID: ([[:digit:]]+)/\1/p'`; do \
    hammer content-view publish --organization "$(ORG_NAME)" --id $$cid; \
done

PUBLISH_AND_PROMOTE_CONTENT_VIEWS = \
for cid in \
    `hammer --output yaml content-view list --organization "$(ORG_NAME)" --nondefault 1 | \
     sed -nr 's/.*Content View ID: ([[:digit:]]+)/\1/p'`; do \
    hammer content-view publish --organization "$(ORG_NAME)" --id $$cid && \
    latest_ver=`hammer --output yaml content-view version list \
                       --organization "$(ORG_NAME)" --content-view-id $$cid | \
         sed -nr 's/.*Version: (.+)/\1/p' | sort -rn | head -n 1` && \
    for lep in $(LIFECYCLE_ENVIRONMENT_PATHS); do \
        hammer content-view version promote --content-view-id $$cid \
	    --organization "$(ORG_NAME)" --version "$$latest_ver" \
	    --to-lifecycle-environment "$$lep"; \
    done; \
done


all:
	@echo "Usage: make (check | install | setup | sync | publish | promote)"


$(LOGDIR):
	mkdir -p $(LOGDIR)

check: check.stamp
check.stamp: $(LOGDIR)
	$(CHECK_CLOCK)
	$(CHECK_FQDN)
	$(CHECK_CDN_ACCESS)
	touch $@

install: install.stamp
install.stamp: check.stamp
	$(SETUP_RHN)
	$(SETUP_SATELLITE_ISO)
	$(INSTALL_SATELLITE_RPMS)
	$(CONFIGURE_BEFORE_SATELLITE_INSTALLATION)
	$(INSTALL_SATELLITE)
	touch $@

setup: setup.stamp
setup.stamp:
	test -f install.stamp
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
	$(SYNC_REPOS_BY_PRODUCT)

publish:
	$(PUBLISH_REPOS)

promote:
	$(PUBLISH_AND_PROMOTE_CONTENT_VIEWS)

akeys:
	$(SETUP_ACTIVATION_KEYS)


.PHONY: check install setup sync publish promote akeys
# vim:noet:

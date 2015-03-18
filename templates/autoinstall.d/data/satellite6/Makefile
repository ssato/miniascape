# Makefile to install and setup Satellite-6.
WORKDIR ?= /root/setup

# '' (empty) or 'yes'
TO_INSTALL_ONLINE ?=
IS_RHEL_7 = $(if $(shell ls /etc/systemd 2>/dev/null || :),yes,)

SATELLITE_ISO_URL ?= {{ satellite.iso_url|default('') }}
SATELLITE_ISO ?= \
$(WORKDIR)/$(if $(SATELLITE_ISO_URL),$(notdir $(SATELLITE_ISO_URL)),satellite.iso)

# RHN related:
RHSM_REGISTER_IF_NOT ?= subscription-manager register || :
RHSM_SUBSCRIPTION_POOL ?= {{ rhn.subscription.pool if rhn.subscription and rhn.subscription.pool }}
RHSM_SUBSCRIBE ?= subscription-manager subscribe \
$(if $(RHSM_SUBSCRIPTION_POOL),--pool=$(RHSM_SUBSCRIPTION_POOL),--auto)
RHSM_SUBSCRIBE_IF_NOT = subscription-manager repos || $(RHSM_SUBSCRIBE)

RHSM_ENABLE_REPOS = \
subscription-manager repos --disable '*' && \
subscription-manager repos \
$(if $(IS_RHEL_7),--enable rhel-7-server-rpms \
--enable rhel-server-rhscl-7-rpms \
--enable rhel-server-7-satellite-6.0-rpms,\
--enable rhel-6-server-rpms \
--enable rhel-server-rhscl-6-rpms \
--enable rhel-6-server-satellite-6.0-rpms)

# See also: Satellite 6.0 Installation, 2.2. Installing Red Hat Satellite with
# an ISO Image: http://red.ht/1wICPsd
INSTALL_RPMS_ONLINE = yum install -y katello
INSTALL_RPMS_FROM_ISO = \
test -f $(SATELLITE_ISO) || curl -o $(SATELLITE_ISO) $(SATELLITE_ISO_URL); \
trap "umount /mnt" INT TERM && \
mount -o ro,loop $(SATELLITE_ISO) /mnt && \
cd /mnt && ./install_packages && cd - && umount /mnt

INSTALL_RPMS = \
$(if $(TO_INSTALL_ONLINE),$(INSTALL_RPMS_ONLINE),$(INSTALL_RPMS_FROM_ISO))

KATELLO_INSTALLER_OPTIONS	?= \
{% if satellite.admin is defined -%}
--foreman-admin-username={{ satellite.admin.name|default('admin') }} \
{{ "--foreman-admin-password=%s" % satellite.admin.password if satellite.admin.password }} \
{{ "--foreman-admin-email=%s" % satellite.admin.email if satellite.admin.email }} \
{{ "--foreman-admin-first-name=%s" % satellite.admin.fist_name if satellite.admin.fist_name }} \
{{ "--foreman-admin-last-name=%s" % satellite.admin.fist_name if satellite.admin.fist_name }} \
{% endif -%}
{%- if proxy is defined and proxy.fqdn is defined and proxy.fqdn -%}
{{-     "--katello-proxy-url=http://%s" % proxy.fqdn }} \
--katello-proxy-port={{ proxy.port|default('8080') }} \
{{ "--katello-proxy-username=%s" % proxy.username if proxy.username }} \
{{ "--katello-proxy-password=%s" % proxy.password if proxy.password }} \
{% endif -%}
$(NULL)

INSTALL_SATELLITE = \
katello-installer $(KATELLO_INSTALLER_OPTIONS) 2>&1 | tee $(WORKDIR)/katello-installer.log

FIREWALL_CMD ?= firewall-cmd --permanent --direct --add-rule

SETUP_FIREWALL_W_FIREWALLD = \
$(FIREWALL_CMD) ipv4 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner foreman -j ACCEPT && \
$(FIREWALL_CMD) ipv6 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner foreman -j ACCEPT && \
$(FIREWALL_CMD) ipv4 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner katello -j ACCEPT && \
$(FIREWALL_CMD) ipv6 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner katello -j ACCEPT && \
$(FIREWALL_CMD) ipv4 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner root -j ACCEPT && \
$(FIREWALL_CMD) ipv6 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner root -j ACCEPT && \
$(FIREWALL_CMD) ipv4 filter OUTPUT 1 -o lo -p tcp -m tcp --dport 9200 -j DROP && \
$(FIREWALL_CMD) ipv6 filter OUTPUT 1 -o lo -p tcp -m tcp --dport 9200 -j DROP

SETUP_FIREWALL_W_IPTABLES = \
iptables -I INPUT -m state --state NEW -p tcp --dport 443 -j ACCEPT && \
iptables -I INPUT -m state --state NEW -p tcp --dport 5671 -j ACCEPT && \
iptables -I INPUT -m state --state NEW -p tcp --dport 80 -j ACCEPT && \
iptables -I INPUT -m state --state NEW -p tcp --dport 8140 -j ACCEPT && \
iptables -I INPUT -m state --state NEW -p tcp --dport 9090 -j ACCEPT && \
iptables -I INPUT -m state --state NEW -p tcp --dport 8080 -j ACCEPT && \
iptables-save > /etc/sysconfig/iptables

SETUP_FIREWALL = \
$(if $(IS_RHEL_7),$(SETUP_FIREWALL_W_FIREWALLD),$(SETUP_FIREWALL_W_IPTABLES))

# See also: Satellite 6.0 Installation Guide, 1.5. Prerequisites:
# http://red.ht/1EYd1wP
CHECKS	?= \
hostname -f && hostname -s && \
ping -c1 localhost && ping -c1 `hostname -s` && \
ping -c1 `hostname -f` && date

KATELLO_REINDEX = \
katello-service stop && \
systemctl start mongod && \
sudo -u apache pulp-manage-db && \
katello-service start && \
foreman-rake katello:reindex

# see: https://access.redhat.com/solutions/1325953
define update-satellite =
$(RHSM_REGISTER_IF_NOT)
$(RHSM_SUBSCRIBE_IF_NOT)
$(RHSM_ENABLE_REPOS)
yum update -y
$(KATELLO_REINDEX)
endef

INITIAL_SETUP_SCRIPT ?= $(WORKDIR)/initial-setup.sh


all: check

check:
	$(CHECKS)

install:
	$(CHECKS)
	$(SETUP_FIREWALL)
	$(RHSM_REGISTER_IF_NOT)
	$(RHSM_SUBSCRIBE_IF_NOT)
	$(RHSM_ENABLE_REPOS)
	$(INSTALL_RPMS)
	$(INSTALL_SATELLITE)

init:
	bash -ex $(INITIAL_SETUP_SCRIPT) -D

update:
	$(update-satellite)

.PHONY: check install init update

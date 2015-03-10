# Makefile to install and setup Satellite-6.
WORKDIR ?= /root/setup

TO_INSTALL_ONLINE ?= # or yes
IS_RHEL_7 = $(if $(shell ls /etc/systemd 2>/dev/null || :),yes,)

SATELLITE_ISO_URL ?= {{ satellite.iso_url|default('') }}
SATELLITE_ISO ?= \
$(if $(SATELLITE_ISO_URL),$(notdir $(SATELLITE_ISO_URL)),satellite.iso)

# If online:
RHSM_SUBSCRIPTION_POOL ?= {{ rhn.subscription.pool if rhn.subscription }}
RHSM_SUBSCRIBE ?= \
subscription-manager subscribe \
$(if $(RHSM_SUBSCRIPTION_POOL),--pool=$(RHSM_SUBSCRIPTION_POOL),--auto)

# See also: Satellite 6.0 Installation Guide, 1.5. Prerequisites:
# http://red.ht/1EYd1wP
CHECKS	?= \
hostname -f && hostname -s && \
ping -c1 localhost && ping -c1 `hostname -s` && \
ping -c1 `hostname -f` && date

# See also: Satellite 6.0 Installation, 2.2. Installing Red Hat Satellite with
# an ISO Image: http://red.ht/1wICPsd
INSTALL_FROM_ISO_IMAGE = \
cd $(WORKDIR) && \
test -f $(SATELLITE_ISO) || curl -O $(SATELLITE_ISO_URL) && \
trap "umount /mnt" INT TERM && \
mount -o ro,loop $(WORKDIR)/$(SATELLITE_ISO) /mnt && \
cd /mnt && ./install_packages && cd - && umount /mnt

SM_ENABLE_REPOS_OPTIONS = \
$(if $(IS_RHEL_7),--enable rhel-7-server-rpms \
--enable rhel-server-rhscl-7-rpms \
--enable rhel-server-7-satellite-6.0-rpms,\
--enable rhel-6-server-rpms \
--enable rhel-server-rhscl-6-rpms \
--enable rhel-6-server-satellite-6.0-rpms)

INSTALL_ONLINE = \
subscription-manager identity || $(RHSM_SUBSCRIBE) && \
subscription-manager repos --disable '*' && \
$(SM_ENABLE_REPOS) && \
yum install -y katello

INSTALL = \
$(if $(TO_INSTALL_ONLINE),$(INSTALL_ONLINE),$(INSTALL_FROM_ISO_IMAGE))

KATELLO_INSTALLER_OPTIONS	?= \
{% if satellite.admin is defined -%}
--foreman-admin-username={{ satellite.admin.name|default('admin') }} \
{{ "--foreman-admin-password=%s" % satellite.admin.password if satellite.admin.password }} \
{{ "--foreman-admin-email=%s" % satellite.admin.email if satellite.admin.email }} \
{{ "--foreman-admin-first-name=%s" % satellite.admin.fist_name if satellite.admin.fist_name }} \
{{ "--foreman-admin-last-name=%s" % satellite.admin.fist_name if satellite.admin.fist_name }} \
{% endif -%}
{%- if proxy.fqdn is defined and proxy.fqdn -%}
{{-     "--katello-proxy-url=http://%s" % proxy.fqdn }} \
--katello-proxy-port={{ proxy.port|default('8080') }} \
{{ "--katello-proxy-username=%s" % proxy.username if proxy.username }} \
{{ "--katello-proxy-password=%s" % proxy.password if proxy.password }} \
{% endif -%}
$(NULL)

SETUP_FIREWALL_W_FIREWALLD = \
firewall-cmd --permanent --direct --add-rule ipv4 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner foreman -j ACCEPT && \
firewall-cmd --permanent --direct --add-rule ipv6 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner foreman -j ACCEPT && \
firewall-cmd --permanent --direct --add-rule ipv4 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner katello -j ACCEPT && \
firewall-cmd --permanent --direct --add-rule ipv6 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner katello -j ACCEPT && \
firewall-cmd --permanent --direct --add-rule ipv4 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner root -j ACCEPT && \
firewall-cmd --permanent --direct --add-rule ipv6 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner root -j ACCEPT && \
firewall-cmd --permanent --direct --add-rule ipv4 filter OUTPUT 1 -o lo -p tcp -m tcp --dport 9200 -j DROP && \
firewall-cmd --permanent --direct --add-rule ipv6 filter OUTPUT 1 -o lo -p tcp -m tcp --dport 9200 -j DROP

SETUP_FIREWALL_W_IPTABLES = \
iptables -I INPUT -m state --state NEW -p tcp --dport 443 -j ACCEPT \
&& iptables -I INPUT -m state --state NEW -p tcp --dport 5671 -j ACCEPT \
&& iptables -I INPUT -m state --state NEW -p tcp --dport 80 -j ACCEPT \
&& iptables -I INPUT -m state --state NEW -p tcp --dport 8140 -j ACCEPT \
&& iptables -I INPUT -m state --state NEW -p tcp --dport 9090 -j ACCEPT \
&& iptables -I INPUT -m state --state NEW -p tcp --dport 8080 -j ACCEPT \
iptables-save > /etc/sysconfig/iptables

SETUP_FIREWALL = \
$(if $(IS_RHEL_7),$(SETUP_FIREWALL_W_FIREWALLD),$(SETUP_FIREWALL_W_IPTABLES))

KATELLO_REINDEX = \
katello-service stop && \
systemctl start mongod && \
sudo -u apache pulp-manage-db && \
katello-service start && \
foreman-rake katello:reindex

# see: https://access.redhat.com/solutions/1325953
UPDATE_TO_THE_LATEST = \
subscription-manager identity || $(RHSM_SUBSCRIBE) && \
subscription-manager repos \
--enable $(if $(IS_RHEL_7),rhel-server-6-satellite-6.0-rpms,rhel-6-server-satellite-6.0-rpms) && \ 
yum update -y && \
$(KATELLO_REINDEX)


all: check

check:
	$(CHECKS)

install:
	$(CHECKS)
	$(INSTALL)
	$(SETUP_FIREWALL)
	katello-installer $(KATELLO_INSTALLER_OPTIONS) 2>&1 | tee katello-installer.log

update:
	$(UPDATE_TO_THE_LATEST)

.PHONY: check install update

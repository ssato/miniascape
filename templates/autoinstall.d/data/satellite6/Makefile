# Makefile to install and setup Satellite-6.
WORKDIR ?= /root/setup

TO_INSTALL_ONLINE ?= no  # or yes

SATELLITE_ISO_URL ?= {{ satellite.iso_url|default('') }}
SATELLITE_ISO ?= $(notdir $(SATELLITE_ISO_URL))

# If online:
RHSM_SUBSCRIPTION_POOL ?= {{ rhn.subscription.pool if rhn.subscription }}
RHSM_SUBSCRIBE ?= \
subscription-manager subscribe \
$(if $(RHSM_SUBSCRIPTION_POOL),--pool=$(RHSM_SUBSCRIPTION_POOL),--auto)

# See also: Satellite 6.0 Installation Guide, 1.5. Prerequisites:
# http://red.ht/1EYd1wP
CHECKS	?= ping -c1 localhost && ping -c1 `hostname -s` && \
ping -c1 `hostname -f` && date

# See also: Satellite 6.0 Installation, 2.2. Installing Red Hat Satellite with
# an ISO Image: http://red.ht/1wICPsd
define install-offline =
cd $(WORKDIR) && \
test -f $(SATELLITE_ISO) || curl -O $(SATELLITE_ISO_URL)
trap "umount /mnt" INT TERM && \
mount -o ro,loop $(WORKDIR)/$(SATELLITE_ISO) /mnt && \
cd /mnt && ./install_packages && cd - && umount /mnt
endef

define install-online =
subscription-manager identity || $(RHSM_SUBSCRIBE)
subscription-manager repos --disable '*'
subscription-manager repos --enable rhel-7-server-rpms \
			   --enable rhel-server-rhscl-7-rpms \
			   --enable rhel-server-7-satellite-6.0-rpms
yum install -y katello
endef

KATELLO_INSTALLER_OPTIONS	?= \
{%- if proxy.fqdn is defined and proxy.fqdn -%}
{{-     "--katello-proxy-url=http://%s" % proxy.fqdn }} \
--katello-proxy-port={{ proxy.port|8080 }} \
{{ "--katello-proxy-username=%s" % proxy.username if proxy.username }} \
{{ "--katello-proxy-password=%s" % proxy.password if proxy.password }} \
{%- endif -%}
$(NULL)

define setup-firewall =
firewall-cmd --permanent --direct --add-rule ipv4 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner foreman -j ACCEPT
firewall-cmd --permanent --direct --add-rule ipv6 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner foreman -j ACCEPT
firewall-cmd --permanent --direct --add-rule ipv4 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner katello -j ACCEPT
firewall-cmd --permanent --direct --add-rule ipv6 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner katello -j ACCEPT
firewall-cmd --permanent --direct --add-rule ipv4 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner root -j ACCEPT
firewall-cmd --permanent --direct --add-rule ipv6 filter OUTPUT 0 -o lo -p tcp -m tcp --dport 9200 -m owner --uid-owner root -j ACCEPT
firewall-cmd --permanent --direct --add-rule ipv4 filter OUTPUT 1 -o lo -p tcp -m tcp --dport 9200 -j DROP
firewall-cmd --permanent --direct --add-rule ipv6 filter OUTPUT 1 -o lo -p tcp -m tcp --dport 9200 -j DROP
endef



all: check

check:
	$(CHECKS)

install:
	$(CHECKS)
ifeq ($(TO_INSTALL_ONLINE),yes)
	$(install-online)
else
	$(install-offline)
endif
	katello-installer $(KATELLO_INSTALLER_OPTIONS)
	$(setup-firewall)

.PHONY: check install

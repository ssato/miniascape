# Makefile to install and setup Satellite-6.
# see also: Satellite 6 MDP Installation Guide, http://red.ht/18lfMdC
WORKDIR ?= /root/setup
SATELLITE_ISO ?= Satellite-6.0.3-RHEL-6-20140630.0-Satellite-x86_64-dvd1.iso
SATELLITE_ISO_URL = {{ satellite.iso_url|default('') }}
SUBSCRIPTION_POOL_ID = {{ subscription_pool_id|default('') }}

#CONFIGURE_OPTS ?= --user-name=admin --user-pass={{ satellite.admin.password|default('secret') }}{% if satellite.admin.org_name is defined %}--org-name={{ satellite.admin.org_name }}{% endif %}
CONFIGURE_OPTS ?= --answer-file=$(WORKDIR)/answers.txt

check:
	ping -c1 localhost
	ping -c1 `hostname -s`
	ping -c1 `hostname -f`

install: check
	test -f $(SATELLITE_ISO) || curl -O $(SATELLITE_ISO_URL)
	trap "umount /mnt" INT TERM && mount -o ro,loop $(SATELLITE_ISO) /mnt && cd /mnt && ./install_packages && cd - && umount /mnt

install-online: check
	test -n "$(SUBSCRIPTION_POOL_ID)" && subscription-manager subscribe --pool=$(SUBSCRIPTION_POOL_ID)
	subscription-manager repos --disable "*"
	subscription-manager repos --enable rhel-6-server-rpms \
				   --enable rhel-server-rhscl-6-rpms \
				   --enable rhel-server-6-satellite-6-beta-rpms
	yum install -y katello

setup:
	sed -i.save -e 's,:answer_file: /etc/katello-installer/answers.katello-installer.yaml,:answer_file: /root/setup/answers.txt,g' /etc/katello-installer/katello-installer.yaml
	katello-installer

.PHONY: check install install-online setup

# Makefile to install and setup Satellite-6.
# see also: Satellite 6 MDP Installation Guide, http://red.ht/18lfMdC
WORKDIR ?= /root/setup
SATELLITE_ISO ?= Satellite-6.0.1-RHEL-6-20130807.0-Satellite-x86_64-dvd1.iso

#CONFIGURE_OPTS ?= --user-name=admin --user-pass={{ katello.password|default('secret') }}{% if katello.org_name is defined %}--org-name={{ katello.org_name }}{% endif %}
CONFIGURE_OPTS ?= --answer-file=$(WORKDIR)/answers.txt


check: check.stamp
check.stamp:
	ping -c1 localhost
	ping -c1 `hostname -s`
	ping -c1 `hostname -f`
	touch $@

install:
	trap "umount /mnt" INT TERM && mount -o ro,loop $(SATELLITE_ISO) /mnt && cd /mnt && ./install_packages.sh && cd - && umount /mnt

setup:
	katello-configure $(CONFIGURE_OPTS)

.PHONY: check install setup

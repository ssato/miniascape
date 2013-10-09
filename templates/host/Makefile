# Makefile to setup libvirt host.

DESTDIR =
CURDIR = $(shell pwd)

REGISTER_NET = $(CURDIR)/usr/libexec/miniascape/register_libvirt_network.sh
INSTALL_DATA = install -m 644


setup-network:
	{% for net in networks %}bash -x $(REGISTER_NET) {{ net }}
	{% endfor %}

install:
	mkdir -p $(DESTDIR)/etc/modprobe.d
	mkdir -p $(DESTDIR)/etc/httpd/conf.d
	mkdir -p $(DESTDIR)/etc/auto.master.d
	mkdir -p $(DESTDIR)/usr/share/miniascape/networks.d
	{% for net in networks %}$(INSTALL_DATA) $(CURDIR)/usr/share/miniascape/networks.d/{{ net }}.xml $(DESTDIR)/usr/share/miniascape/networks.d
	{% endfor %}
	$(INSTALL_DATA) $(CURDIR)/etc/modprobe.d/kvm.conf $(DESTDIR)/etc/modprobe.d
	$(INSTALL_DATA) $(CURDIR)/etc/fence_virt.conf $(DESTDIR)/etc
	$(INSTALL_DATA) $(CURDIR)/etc/httpd/conf.d/miniascape_autoinst.conf $(DESTDIR)/etc/httpd/conf.d
	$(INSTALL_DATA) $(CURDIR)/etc/auto.master.d/isos.autofs $(DESTDIR)/etc/auto.master.d/isos.autofs
	$(INSTALL_DATA) $(CURDIR)/etc/auto.iso $(DESTDIR)/etc

.PHONY: setup-network install

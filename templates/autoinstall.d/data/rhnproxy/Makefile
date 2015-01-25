# Makefile to install RH Satellite Proxy
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup
ANSTXT ?= $(WORKDIR)/answers.txt

# see also: Satellite Proxy Installation Guide,
# 3.5. Installing the Red Hat Satellite Proxy Server Packages:
# http://red.ht/1D6gLeL
define install_rhnproxy =
yum repolist | grep -E '^rhn-tools-rhel-x86_64-server-6'
yum repolist | grep -E '^redhat-rhn-proxy-5.7-server-x86_64-6'
yum install -y spacewalk-proxy-installer
test -d /root/ssl-build || mkdir /root/ssl-build
scp 'root@{{ rhnproxy.parent }}:/root/ssl-build/{RHN-ORG-PRIVATE-SSL-KEY,RHN-ORG-TRUSTED-SSL-CERT,rhn-ca-openssl.cnf}' /root/ssl-build
configure-proxy.sh --answer-file=$(ANSTXT)
endef

all: check install

check: $(WORKDIR)/check.stamp
$(WORKDIR)/check.stamp:
	date
	fqdn=`hostname -f`; test "x$$fqdn" = 'x{{ fqdn }}'
	touch $@

# NOTE: It must register to RHN hosted or RH Satellite, that is,
# /etc/sysconfig/rhn/systemid must exist before RH Proxy installation.
install: $(WORKDIR)/install.stamp
$(WORKDIR)/install.stamp: /etc/sysconfig/rhn/systemid $(ANSTXT)
	$(install_rhnproxy)
	touch $@

.PHONY: check install


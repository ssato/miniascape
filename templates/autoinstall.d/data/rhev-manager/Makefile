# Makefile to install and setup RHEV-M
# Author: Satoru SATOH <ssato @ redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup
ANSTXT ?= $(WORKDIR)/answers.txt

#
# Prepare activation keys which required software channels below
# to install rhevm RPMs from RHN.
#
# Required software channels: jbappplatform-6-x86_64-server-6-rpm,
# 	rhel-x86_64-server-6, rhel-x86_64-server-6-rhevm-3.1,
# 	rhel-x86_64-server-supplementary-6, rhel-x86_64-server-6-rhevh
#
RHN_AKEYS ?= {{ rhn.activationkeys }}
RHN_PROFILENAME ?= {% if rhn.profilename is defined and rhn.profilename %}{{ rhn.profilename }}{% else %}$(shell hostname -f)_$(shell date +%Y%m%d_%H_%M_%S){% endif %}

# http://red.ht/UKeD47
define rhn_register =
subscription-manager register --autosubscribe --force
yum-config-manager --enablerepo=jbappplatform-6-x86_64-server-6-rpm --enablerepo=rhel-x86_64-server-6-rhevm-3.1 --enablerepo=rhel-x86_64-server-supplementary-6
endef

# http://red.ht/VKPoiY
nfs_storage_domain_0_dir = /var/lib/exports/guests
mk_nfs_storage_domain_0 = \
  mkdir -p -m 0755 $(nfs_storage_domain_0_dir) && \
  chown -R vdsm:kvm $(nfs_storage_domain_0_dir) && \
  echo '$(nfs_storage_domain_0_dir) *(rw)' >> /etc/exports && \
  service nfs reload


install: $(WORKDIR)/install.stamp
$(WORKDIR)/install.stamp:
	test -f /etc/sysconfig/rhn/systemid || rhnreg_ks --profilename=$(RHN_PROFILENAME) -v --activationkey=$(RHN_AKEYS) --force
	yum -y update
	rpm -q rhevm || yum -y install rhevm
	rpm -q rhevm-cli || yum -y install rhevm-cli
	rpm -q ipa-client || yum -y install ipa-client
	rpm -q rhevm-dwh || yum -y install rhevm-dwh
	rpm -q rhevm-reports || yum -y install rhevm-reports
	$(mk_nfs_storage_domain_0)
	touch $@

$(ANSTXT): $(ANSTXT).first_half $(ANSTXT).last_half
	cat $^ > $@

$(ANSTXT).first_half: $(WORKDIR)/install.stamp
	rhevm-setup --gen-answer-file=$@

setup: $(WORKDIR)/setup.stamp
$(WORKDIR)/setup.stamp: $(ANSTXT)
	rhevm-setup --answer-file=$(ANSTXT)
	touch $@

.PHONY: install setup

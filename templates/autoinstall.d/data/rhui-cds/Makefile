# Makefile to install RHUI RPMs in CDS.
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup

# @see http://red.ht/RAKEyc :
RHUI_ISO ?= RHEL-6-RHUI-2-LATEST-Server-x86_64-DVD.iso

all: $(RHUI_ISO)
	mount -o ro,loop $(RHUI_ISO) /mnt
	cd /mnt && ./install_CDS.sh && cd - && umount /mnt
	touch $@


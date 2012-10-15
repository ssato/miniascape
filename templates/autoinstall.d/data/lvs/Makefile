# Requirements:
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
WORKDIR ?= /root/setup

all:
	@echo "Usage: make [VAR_OVERRIDES ...]"


init.stamp:
	/usr/sbin/piranha-passwd
	/sbin/service piranha-gui restart
	touch $@

clean:


.PHONY: clean

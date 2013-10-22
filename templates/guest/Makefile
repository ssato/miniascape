all: netregist build

netregist: netregist.stamp
netregist.stamp: $(CURDIR)/net_register.sh
	bash -x $< && touch $@

build: netregist.stamp build.stamp
build.stamp: $(CURDIR)/vmbuild.sh
	bash -x $< && touch $@.stmp

.PHONY: netregist build

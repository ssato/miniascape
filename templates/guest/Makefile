all: netregist build

netregist: netregist.stamp
netregist.stamp: net_register.sh
	bash -x $< && touch $@

build: netregist.stamp build.stamp
build.stamp: vmbuild.sh
	bash -x $< && touch $@.stmp

.PHONY: netregist build

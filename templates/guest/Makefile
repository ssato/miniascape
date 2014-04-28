modified_for_test_env ?= {{ test.modified_for_test_env }}

all: netregist build

netregist: netregist.stamp
netregist.stamp: $(CURDIR)/net_register.sh
	bash -x $< && touch $@

build: netregist.stamp build.stamp
build.stamp: $(CURDIR)/vmbuild.sh
	bash -x $< && touch $@.stmp

## For tests:
setup: $(CURDIR)/test.ks.cfg $(CURDIR)/vmbuild-test.sh

$(CURDIR)/test.ks.cfg: $(CURDIR)/ks.cfg
	$(modified_for_test_env) $< > $@.t && mv $@.t $@

$(CURDIR)/vmbuild-test.sh: $(CURDIR)/vmbuild.sh
	sed -e 's/ks.cfg/test.ks.cfg/g' $< | $(modified_for_test_env) > $@.t && mv $@.t $@

.PHONY: netregist build

TOPDIR = .
SITE ?=

miniascape_OPTIONS = -t $(TOPDIR)/templates

ifeq ($(strip $(SITE)),)
$(error Variable SITE must be set!)
endif


all: build

build:
	miniascape b $(miniascape_OPTIONS) -C $(TOPDIR)/$(SITE) -w $(TOPDIR)/out

floppy:
	for d in $(wildcard $(TOPDIR)/out/guests.d/*); do test -d $$d && make -C $$d floppy || :; done

setup:
	for d in $(wildcard $(TOPDIR)/out/guests.d/*); do test -d $$d && make -C $$d setup || :; done 

doc:
	test -d $(TOPDIR)/doc || \
	docutils-exts-bootstrap -w $(TOPDIR)/doc -C '$(TOPDIR)/$(SITE)/*.yml' \
		`anyconfig_cli -T --get doc.name '$(TOPDIR)/$(SITE)/*.yml'` \
		-t `anyconfig_cli -T --get doc.type '$(TOPDIR)/$(SITE)/*.yml'` -D -R

.PHONY: build floppy setup doc

selinuxmoddir	= $(datadir)/selinux/packages/$(PACKAGE)
dist_selinuxmod_DATA	= $(PACKAGE).pp

EXTRA_DIST = $(PACKAGE).te


$(PACKAGE).pp: $(PACKAGE).te
	$(AM_V_GEN)$(MAKE) -f $(SELINUX_MAKEFILE)


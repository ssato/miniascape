devdatadir	= $(pkgdatadir)/devel

dist_sbin_SCRIPTS = vmbuild
dist_devdata_DATA = core.mk vars.mk disk.mk network.mk virtinst.mk rpm.mk vm.spec.in

CLEANFILES = vmbuild core.mk
EXTRA_DIST = core.mk.in vmbuild.in

subst	= $(AM_V_GEN)$(SED) -e 's,[@]pkgdatadir[@],$(pkgdatadir),g' -e 's,[@]pkgsysconfdir[@],$(sysconfdir)/$(PACKAGE),g' $(srcdir)/$< > $@.t && mv $@.t $@

core.mk: core.mk.in
	$(subst)

vmbuild: vmbuild.in
	$(subst)


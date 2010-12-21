devdatadir	= $(pkgdatadir)/devel

dist_sbin_SCRIPTS = vmbuild
dist_devdata_DATA = core.mk disk.mk network.mk virtinst.mk rpm.mk vm.spec.in

CLEANFILES = $(dist_sbin_SCRIPTS)
EXTRA_DIST = vmbuild.in

vmbuild: vmbuild.in
	$(SED) -e 's,[@]pkgdatadir[@],$(pkgdatadir),g' \
		-e 's,[@]pkgsysconfdir[@],$(sysconfdir)/$(PACKAGE),g' \
			$(srcdir)/$< > $@.t && mv $@.t $@


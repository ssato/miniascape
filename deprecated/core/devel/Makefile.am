devdatadir	= $(pkgdatadir)/devel
devdata2dir	= $(devdatadir)

dist_devdata_DATA = vars.mk disk.mk network.mk virtinst.mk rpm.mk vm.spec.in
nodist_sbin_SCRIPTS = vmbuild
nodist_devdata2_DATA = core.mk

CLEANFILES = vmbuild core.mk
EXTRA_DIST = core.mk.in vmbuild.in

subst	= $(AM_V_GEN)$(SED) -e 's,[@]PACKAGE[@],$(PACKAGE),g' -e 's,[@]pkgdatadir[@],$(pkgdatadir),g' \
-e 's,[@]pkgsysconfdir[@],$(sysconfdir)/$(PACKAGE),g' $(srcdir)/$< > $@.t && mv $@.t $@

core.mk: core.mk.in
	$(subst)

vmbuild: vmbuild.in
	$(subst)


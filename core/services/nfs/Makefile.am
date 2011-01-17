nfsconfdir = $(sysconfdir)/$(PACKAGE)/nfs
nfsexportdir = /var/lib/$(PACKAGE)/exports

nodist_nfsconf_DATA = exports

EXTRA_DIST	= exports.in
CLEANFILES = exports

subst	= $(AM_V_GEN)$(SED) -e 's,[@]@nfsexportdir[@],$(nfsexportdir),g' -e 's,[@]nfs_networ[@],$(NET_2_NETWORK).0/24,g' $(srcdir)/$< > $@.t && mv $@.t $@

exports: exports.in
	$(subst)

install-data-hook:
	$(MKDIR_P) $(DESTDIR)$(nfsexportdir)


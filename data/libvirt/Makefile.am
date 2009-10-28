libvirtnetworkdir = @sysconfdir@/@PACKAGE@/libvirt/networks
dist_libvirtnetwork_DATA = net-1.xml net-2.xml net-3.xml

CLEANFILES = $(dist_libvirtnetwork_DATA)

install-data-hook:
	$(MKDIR_P) $(DESTDIR)@sysconfdir@/@PACKAGE@/libvirt/domains


libvirtnetworkdir = @sysconfdir@/@PACKAGE@/libvirt/networks
dist_libvirtnetwork_DATA = net-1.xml net-2.xml net-3.xml

CLEANFILES = $(dist_libvirtnetwork_DATA)

net-%.xml: net-%.xml.in
	@PYTHON@ $(abs_top_srcdir)/src/netxml-del-dhcp.py -o $@ $<

install-data-hook:
	$(MKDIR_P) $(DESTDIR)@sysconfdir@/@PACKAGE@/libvirt/domains


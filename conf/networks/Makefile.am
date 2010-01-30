netconfdir = @sysconfdir@/@PACKAGE@/networks
netconfxmldir = @localstatedir@/lib/@PACKAGE@/networks
dist_netconf_DATA = net-1.yaml net-2.yaml net-3.yaml

DISTCLEANFILES = net-1.yaml net-2.yaml net-3.yaml

install-data-hook:
	$(MKDIR_P) $(DESTDIR)$(netconfxmldir)

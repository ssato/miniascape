netdatadir = $(datadir)/libvirt/networks

dist_netdata_DATA = net-1.xml net-2.xml hosts.add

hosts.add: net-1.xml net-2.xml
	$(AM_V_GEN)$(SED) -nre 's,.*name="([^.]+).([^"]+)" ip="([^"]+)".*,\3 \1.\2 \1,p' $^ > $@

CLEANFILES	= hosts.add 

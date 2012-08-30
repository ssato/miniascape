netdatadir = $(datadir)/libvirt/networks

nodist_netdata_DATA = net-1.xml net-2.xml hosts.add

hosts.add: net-1.xml
	$(AM_V_GEN)$(SED) -nre 's,.*name="([^"]+)" ip="([^"]+)".*,\2 \1.$(NET_1_DOMAIN) \1,p' $< > $@

CLEANFILES	= hosts.add 

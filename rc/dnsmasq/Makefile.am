dnsmasqinitdir = @sysconfdir@/rc.d/init.d
dist_dnsmasqinit_SCRIPTS = dnsmasq-net-1 dnsmasq-net-2 dnsmasq-net-3

DISTCLEANFILES = $(dist_dnsmasqinit_SCRIPTS)


dnsmasq-net-2: dnsmasq-net-1
	sed -e 's,net-1,net-2,g' $< > $@

dnsmasq-net-3: dnsmasq-net-1
	sed -e 's,net-1,net-3,g' $< > $@


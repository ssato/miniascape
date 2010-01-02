dnsmasqconfdir = @sysconfdir@/@PACKAGE@/dnsmasq
dnsmasqhostsfiledir = @localstatedir@/lib/@PACKAGE@/dnsmasq
dnsmasqinitdir = @sysconfdir@/rc.d/init.d

dist_dnsmasqconf_DATA = net-1.conf net-2.conf net-3.conf
dist_dnsmasqhostsfile_DATA = net-1.hostsfile net-2.hostsfile net-3.hostsfile
dist_dnsmasqinit_SCRIPTS = @PACKAGE@-net-1 @PACKAGE@-net-2 @PACKAGE@-net-3

CLEANFILES = $(dist_dnsmasqconf_DATA) \
$(dist_dnsmasqhostsfile_DATA) $(dist_dnsmasqinit_SCRIPTS)

netgen = @PYTHON@ $(abs_top_srcdir)/src/netconf_gen.py -T dnsmasq


net-%.hostsfile: net-%.conf
net-%.conf: $(abs_top_builddir)/data/libvirt/net-%.xml.in
	$(netgen) -o $@ $<

@PACKAGE@-net-2: @PACKAGE@-net-1
	sed -e 's,net-1,net-2,g' $< > $@

@PACKAGE@-net-3: @PACKAGE@-net-1
	sed -e 's,net-1,net-3,g' $< > $@

install-data-hook:
	$(MKDIR_P) $(DESTDIR)@localstatedir@/run/@PACKAGE@/dnsmasq


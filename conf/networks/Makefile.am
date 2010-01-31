netconfdir = @sysconfdir@/@PACKAGE@/networks
netxmldir = @localstatedir@/lib/@PACKAGE@/networks
dnsmasqdir = $(netxmldir)/dnsmasq

dist_netconf_DATA = net-1.yaml net-2.yaml net-3.yaml
dist_netxml_DATA = net-1.xml net-2.xml net-3.xml
dist_dnsmasq_DATA = net-1.conf net-2.conf net-3.conf \
net-1.hostsfile net-2.hostsfile net-3.hostsfile

DISTCLEANFILES = $(dist_netconf_DATA)
CLEANFILES = $(dist_netxml_DATA) $(dist_dnsmasq_DATA)


abs_top_srcdir	?= $(abs_srcdir)/../..
net_configure	= $(PYTHON) $(abs_top_srcdir)/src/net-configure.py
netxml_tmpl	= $(abs_top_srcdir)/data/templates/networks/net-x.xml.tmpl
dnsmasqcnf_tmpl	= $(abs_top_srcdir)/data/templates/networks/dnsmasq/net-x.conf.tmpl
dnsmasqhsf_tmpl	= $(abs_top_srcdir)/data/templates/networks/dnsmasq/net-x.hostsfile.tmpl

net_compile	= $(net_configure) --conf $< --netxml-template $(netxml_tmpl) --dnsmasq-conf-template $(dnsmasqcnf_tmpl) --dnsmasq-hostsfile-template $(dnsmasqhsf_tmpl)


net-1.conf net-1.hostsfile: net-1.xml
net-1.xml: net-1.yaml
	$(net_compile) --netxml $@ --dnsmasq-conf net-1.conf --dnsmasq-hostsfile net-1.hostsfile net-1

net-2.conf net-2.hostsfile: net-2.xml
net-2.xml: net-2.yaml
	$(net_compile) --netxml $@ --dnsmasq-conf net-2.conf --dnsmasq-hostsfile net-2.hostsfile net-2

net-3.conf net-3.hostsfile: net-3.xml
net-3.xml: net-3.yaml
	$(net_compile) --netxml $@ --dnsmasq-conf net-3.conf --dnsmasq-hostsfile net-3.hostsfile net-3




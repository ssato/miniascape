templatesdir = @datadir@/@PACKAGE@/templates/networks
dist_templates_DATA = net-x.xml.tmpl

SUBDIRS = dnsmasq


temploutdir = @localstatedir@/lib/@PACKAGE@/networks
install-data-hook:
	$(MKDIR_P) $(temploutdir)


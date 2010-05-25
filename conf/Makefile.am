SUBDIRS = kickstart networks fenced

dist_pkgsysconf_DATA = config
pkgsysconfdir	= @sysconfdir@/@PACKAGE@


config: config.in
	sed -e 's,@@pkgsysconfdir@@,$(sysconfdir)/$(PACKAGE),g' \
		-e 's,@@pkgdatadir@@,$(datadir)/$(PACKAGE),g' \
		$< > $@


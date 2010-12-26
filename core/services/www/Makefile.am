if USE_NGINX
wwwconf	= nginx_miniascape.conf
wwwconfdir	= $(sysconfdir)/nginx/conf.d
wwwsubconfdir	= $(wwwconfdir)/m

install-data-hook:
	$(MKDIR_P) $(DESTDIR)$(wwwsubconfdir)

else
wwwconf	= apache_miniascape.conf
wwwconfdir	= $(sysconfdir)/httpd/conf.d
endif


dist_wwwconf_DATA	= $(wwwconf)

CLEANFILES	= $(wwwconf)
EXTRA_DIST	= $(wwwconf).in

$(wwwconf): $(wwwconf).in
	$(AM_V_GEN)$(SED) -e 's,[@]pkgdatadir[@],$(datadir)/$(PACKAGE),g' \
		-e 's,[@]NET_1_NETWORK[@],$(NET_1_NETWORK),g' \
		$(srcdir)/$< > $@.t && mv $@.t $@


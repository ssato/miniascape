if USE_NGINX
wwwconfdir	= $(sysconfdir)/nginx/conf.d/m
wwwconf_SOURCE	= nginx.conf
else
wwwconfdir	= $(sysconfdir)/httpd/conf.d
wwwconf_SOURCE	= apache.conf
endif

wwwconf	= miniascape-datasrc-dvd.conf

nodist_wwwconf_DATA	= $(wwwconf)

CLEANFILES	= $(wwwconf)
EXTRA_DIST	= apache.conf nginx.conf

$(wwwconf): $(wwwconf_SOURCE)
	$(AM_V_GEN)$(SED) -e 's,[@]WWWDATADIR[@],$(WWWDATADIR),g' \
		-e 's,[@]AUTOINST_NETWORK[@],$(AUTOINST_NETWORK),g' \
		$(srcdir)/$< > $@.t && mv $@.t $@

install-data-hook:
	$(MKDIR_P) $(DESTDIR)/$(WWWDATADIR)

if USE_NGINX
wwwconfdir	= $(sysconfdir)/nginx/conf.d
wwwconf_SOURCE	= nginx.conf
else
wwwconfdir	= $(sysconfdir)/httpd/conf.d
wwwconf_SOURCE	= apache.conf
endif

wwwconf	= miniascape.conf
nodist_wwwconf_DATA	= $(wwwconf)

CLEANFILES	= $(wwwconf)
EXTRA_DIST	= apache.conf nginx.conf

$(wwwconf): $(wwwconf_SOURCE)
	$(AM_V_GEN)$(SED) \
		-e 's,[@]AUTOINSTDATADIR[@],$(datadir)/$(PACKAGE)/autoinst,g' \
		-e 's,[@]ISOMNTDIR[@],$(ISOMNTDIR),g' \
		-e 's,[@]AUTOINST_NETWORK[@],$(NET_1_NETWORK),g' \
		$(srcdir)/$< > $@.t && mv $@.t $@

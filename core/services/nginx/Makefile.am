if USE_NGINX
websysconfdir = @sysconfdir@/nginx/conf.d
websubsysconfdir = $(websysconfdir)/m
dist_websysconf_DATA = @PACKAGE@.conf

install-data-hook:
	@MKDIR_P@ $(DESTDIR)$(websubsysconfdir)
endif

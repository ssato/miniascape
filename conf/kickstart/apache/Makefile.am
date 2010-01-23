apacheconfdir = @sysconfdir@/httpd/conf.d

if HTTPD_BACKEND_APACHE
dist_apacheconf_DATA = kickstart.conf kickstart-dvd.conf
else
dist_apacheconf_DATA =
endif

CLEANFILES = $(dist_apacheconf_DATA)

EXTRA_DIST = $(PACKAGE).spec rpm.mk

SUBDIRS  = devel services tools vm

include $(abs_srcdir)/rpm.mk

pkgsysconfdir = $(sysconfdir)/$(PACKAGE)
dist_pkgsysconf_DATA = config

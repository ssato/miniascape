AUTOMAKE_OPTIONS = foreign
EXTRA_DIST = @PACKAGE@.spec.in
ACLOCAL_AMFLAGS = -I aux/m4

SUBDIRS  = aux data etc miniascape src tests

if USE_RPM
include $(abs_top_srcdir)/aux/rpm.mk
endif

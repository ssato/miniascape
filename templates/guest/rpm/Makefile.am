EXTRA_DIST = package.spec rpm.mk
include $(abs_top_srcdir)/rpm.mk

devdatadir = {{ guests_build_datadir|default('/usr/share/miniascape/build/guests') }}

guests.mk:
	for d in *; do \
		test -d $$d && \
		dataid=$(subst -,,$$d) && \
		echo "pkgdata$${dataid} = $(devdatadir)/$$d" >> $@.t && \
		echo "dist_pkgdata$${dataid}_DATA = $$d/ks.cfg $$d/net_register.sh $$d/vmbuild.sh" >> $@.t && \
		echo "" >> $@.t; \
	done
	mv $@.t $@

include guests.mk

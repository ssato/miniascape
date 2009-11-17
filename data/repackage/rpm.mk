rpmdir = $(abs_builddir)/rpm

rpmdirs: 
	mkdir -p $(rpmdir)/{RPMS,SRPMS,BUILD,BUILDROOT,SOURCES}

DIST_ZIP = xz
ifeq ($(DIST_ZIP),bzip2)
RPM_SOURCE0_SUFFIX = bz2
else
RPM_SOURCE0_SUFFIX = $(DIST_ZIP)
endif


rpm: vm-image.spec dist-$(DIST_ZIP) rpmdirs
	cp -f $(abs_builddir)/$(PACKAGE)-$(VERSION).tar.$(RPM_SOURCE0_SUFFIX) $(rpmdir)/SOURCES/
	rpmbuild --define "_topdir $(rpmdir)" \
		--define "_buildroot $(rpmdir)/BUILDROOT" \
		-bb vm-image.spec
	mv $(rpmdir)/RPMS/$(ARCH)/* $(abs_builddir)

srpm: vm-image.spec dist-$(DIST_ZIP) rpmdirs
	cp -f $(abs_builddir)/$(PACKAGE)-$(VERSION).tar.$(RPM_SOURCE0_SUFFIX) $(rpmdir)/SOURCES/
	rpmbuild --define "_topdir $(rpmdir)" \
		--define "_buildroot $(rpmdir)/BUILDROOT" \
		-bs vm-image.spec
	mv $(rpmdir)/SRPMS/* $(abs_builddir)

.PHONY: rpm srpm rpmdirs

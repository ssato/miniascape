rpmdir = $(abs_builddir)/rpm

rpmdirs: 
	mkdir -p $(rpmdir)/{RPMS,SRPMS,BUILD,BUILDROOT,SOURCES}

DIST_ZIP = bzip2
ifeq ($(DIST_ZIP),bzip2)
RPM_SOURCE0_SUFFIX = bz2
else
RPM_SOURCE0_SUFFIX = $(DIST_ZIP)
endif


rpm: virt-domain.spec dist-$(DIST_ZIP) rpmdirs
	cp -f $(abs_builddir)/$(PACKAGE)-$(VERSION).tar.$(RPM_SOURCE0_SUFFIX) $(rpmdir)/SOURCES/
	rpmbuild --define "_topdir $(rpmdir)" \
		--define "_buildroot $(rpmdir)/BUILDROOT" \
		-bb virt-domain.spec
	mv $(rpmdir)/RPMS/noarch/* $(abs_builddir)

srpm: virt-domain.spec dist rpmdirs
	cp -f $(abs_builddir)/$(PACKAGE)-$(VERSION).tar.$(RPM_SOURCE0_SUFFIX) $(rpmdir)/SOURCES/
	rpmbuild --define "_topdir $(rpmdir)" \
		--define "_buildroot $(rpmdir)/BUILDROOT" \
		-bs virt-domain.spec
	mv $(rpmdir)/SRPMS/* $(abs_builddir)

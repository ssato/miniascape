rpmdir = $(abs_builddir)/rpm
rpmdirs = $(addprefix $(rpmdir)/, RPMS SRPMS BUILD BUILDROOT SOURCES SPECS)
rpmspec = $(PACKAGE).spec


$(rpmdirs): 
	$(MKDIR_P) $@

rpm: $(rpmspec) dist-$(SOURCE_ZIP) rpmdirs
	cp -f $(abs_builddir)/$(PACKAGE)-$(VERSION).tar.$(SOURCE_ZIP_EXT) $(rpmdir)/SOURCES/
	$(RPMBUILD) --define "_buildroot $(rpmdir)/BUILDROOT" \
		--define "_topdir $(rpmdir)" -bb $(rpmspec)
	mv $(rpmdir)/RPMS/$(ARCH)/* $(abs_builddir)

srpm: $(rpmspec) dist-$(SOURCE_ZIP) rpmdirs
	cp -f $(abs_builddir)/$(PACKAGE)-$(VERSION).tar.$(SOURCE_ZIP_EXT) $(rpmdir)/SOURCES/
	$(RPMBUILD) --define "_buildroot $(rpmdir)/BUILDROOT" \
		--define "_topdir $(rpmdir)" -bs $(rpmspec)
	mv $(rpmdir)/SRPMS/* $(abs_builddir)

.PHONY: rpm srpm

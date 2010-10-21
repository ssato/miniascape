rpmdir = $(abs_builddir)/rpm
rpmdirs = $(addprefix $(rpmdir)/, RPMS SRPMS BUILD BUILDROOT SOURCES SPECS)
rpmspec = $(PACKAGE).spec

SOURCE_ZIP	?= gzip
SOURCE_ZIP_EXT	?= gz
RPMBUILD_FLAGS	= --define "_buildroot $(rpmdir)/BUILDROOT" --define "_topdir $(rpmdir)"


$(rpmdirs): 
	$(MKDIR_P) $@

rpm: $(rpmspec) dist-$(SOURCE_ZIP) $(rpmdirs)
	cp -f $(abs_builddir)/$(PACKAGE)-$(VERSION).tar.$(SOURCE_ZIP_EXT) $(rpmdir)/SOURCES/
	$(RPMBUILD) $(RPMBUILD_FLAGS) -bb $(rpmspec)
	mv $(rpmdir)/RPMS/*/*.rpm $(abs_builddir)

srpm: $(rpmspec) dist-$(SOURCE_ZIP) $(rpmdirs)
	cp -f $(abs_builddir)/$(PACKAGE)-$(VERSION).tar.$(SOURCE_ZIP_EXT) $(rpmdir)/SOURCES/
	$(RPMBUILD) $(RPMBUILD_FLAGS) -bs $(rpmspec)
	mv $(rpmdir)/SRPMS/*.rpm $(abs_builddir)

.PHONY: rpm srpm

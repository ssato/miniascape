rpmdir = $(abs_builddir)/rpm

rpmdirs: 
	mkdir -p $(rpmdir)/{RPMS,SRPMS,BUILD,BUILDROOT,SOURCES}

rpm: $(PACKAGE).spec dist rpmdirs
	cp -f $(abs_builddir)/$(PACKAGE)-$(VERSION).tar.gz $(rpmdir)/SOURCES/
	rpmbuild --define "_topdir $(rpmdir)" \
		--define "_buildroot $(rpmdir)/BUILDROOT" \
		-bb $(PACKAGE).spec
	mv $(rpmdir)/RPMS/noarch/* $(abs_builddir)

srpm: $(PACKAGE).spec dist rpmdirs
	cp -f $(abs_builddir)/$(PACKAGE)-$(VERSION).tar.gz $(rpmdir)/SOURCES/
	rpmbuild --define "_topdir $(rpmdir)" \
		--define "_buildroot $(rpmdir)/BUILDROOT" \
		-bs $(PACKAGE).spec
	mv $(rpmdir)/SRPMS/* $(abs_builddir)

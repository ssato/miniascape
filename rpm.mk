rpmdir = $(abs_builddir)/rpm
rpmdirs	= $(addprefix $(rpmdir)/,RPMS BUILD BUILDROOT)

rpmbuild = rpmbuild \
--define "_topdir $(rpmdir)" \
--define "_srcrpmdir $(abs_builddir)" \
--define "_sourcedir $(abs_builddir)" \
--define "_buildroot $(rpmdir)/BUILDROOT" \
$(NULL)


$(rpmdirs): 
	$(MKDIR_P) $@

rpm srpm: $(PACKAGE).spec dist-xz $(rpmdirs)

rpm:
	$(rpmbuild) -bb $< && mv $(rpmdir)/RPMS/*/* $(abs_builddir)

srpm:
	$(rpmbuild) -bs $<

.PHONY: rpm srpm

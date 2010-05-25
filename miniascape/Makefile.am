pkgpylibdir = @PYTHON_MODULE_PATH@/@PACKAGE@
dist_pkgpylib_DATA = __init__.py config.py globals.py libvirt.py qemu.py utils.py


EXTRA_DIST = globals.py.in
DISTCLEANFILES = globals.py

globals.py: globals.py.in
	sed -e 's,@@pkgsysconfdir@@,$(sysconfdir)/$(PACKAGE),g' \
		-e 's,@@pkgdatadir@@,$(datadir)/$(PACKAGE),g' \
		$< > $@


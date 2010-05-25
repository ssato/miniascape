pkgpylibdir = @PYTHON_MODULE_PATH@/@PACKAGE@
dist_pkgpylib_DATA = __init__.py config.py globals.py libvirt.py qemu.py utils.py


DISTCLEANFILES = globals.py

globals.py: globals.py.in
	sed 's,@sysconfdir@/@PACKAGE@,$(sysconfdir)/$(PACKAGE),g' $< > $@


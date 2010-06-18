AC_INIT([miniascape],[0.1.99.2])
AC_CONFIG_SRCDIR([miniascape/config.py])
AC_CONFIG_MACRO_DIR([aux/m4])
AM_INIT_AUTOMAKE


AC_PROG_QEMU_IMG dnl 'QEMU_IMG', e.g. /usr/bin/qemu-img.
AC_PROG_VIRSH dnl 'VIRSH', e.g. /usr/bin/virsh.
AC_PROG_SERVICE_LIBVIRTD dnl 'SERVICE_LIBVIRTD', e.g. /etc/rc.d/init.d/libvirtd. 
AC_PROG_PACKAGE_BUILD_TOOL dnl 'PACKAGE_BUILD_TOOL', e.g. /usr/bin/rpmbuild.
AM_CONDITIONAL([USE_RPM],[test "x$USE_RPMBUILD" = xyes])
AC_CHECK_SOURCE_ZIP


AC_ARG_ENABLE([tests],
    [AS_HELP_STRING([--disable-tests],[disable running unit and simplified integration tests])],
    [enable_tests=no],
    [AC_CHECK_PYTHON_MODULE([nose])
     AC_SUBST([MAKE_CHECK],["make check"])])
AM_CONDITIONAL([ENABLE_TESTS],[test "x$enable_tests" != xno])


dnl path parameters
AC_SUBST([_PACKAGE_DATADIR],[`printf ${datadir}/${PACKAGE_NAME}`])
AC_SUBST([_PACKAGE_SYSCONFDIR],[`printf ${sysconfdir}/${PACKAGE_NAME}`])
AC_SUBST([_DOMAIN_XMLDIR],[`printf ${sysconfdir}/${PACKAGE_NAME}/domain.d`])
AC_SUBST([_LIBVIRT_DOMAIN_XMLDIR],[`printf ${sysconfdir}/libvirt/qemu`])
AC_SUBST([_LIBVIRT_NETWORK_XMLDIR],[`printf ${sysconfdir}/libvirt/qemu/networks`])


AC_OUTPUT([
Makefile
miniascape.spec
aux/Makefile
aux/m4/Makefile
data/Makefile
data/templates/Makefile
data/templates/network/Makefile
data/templates/network/dnsmasq/Makefile
data/templates/package/Makefile
data/templates/repackage/Makefile
data/templates/virtinst/Makefile
etc/Makefile
etc/config
miniascape/Makefile
miniascape/globals.py
src/Makefile
src/install-vm
src/net-register
src/net-unregister
src/xpathp
tests/Makefile
tests/globals.py
tests/rhel-5-generic-0.xml
])

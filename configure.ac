AC_INIT([miniascape],[0.1.99])
AM_INIT_AUTOMAKE

AC_PROG_MKDIR_P
AC_PROG_QEMU_IMG
AC_PROG_RPMBUILD
AC_PATH_PROG([PYTHON],[python])
AC_PROG_VIRSH

dnl Disabled for a while; xz is not available on RHEL 5.
dnl AC_CHECK_SOURCE_ZIP
AC_SUBST([SOURCE_ZIP],[gzip])
AC_SUBST([SOURCE_ZIP_EXT],[gz])

dnl FIXME: want to make it configurable
AC_SUBST([PACKAGE_DATA_DIR],[/usr/share/miniascape])
AC_SUBST([PACKAGEFILE_DIR],[/usr/share/miniascape])
AC_SUBST([REPACKAGEFILE_DIR],[/usr/share/miniascape/repackage])
AC_SUBST([ARCH],[noarch])

dnl hwaddr prefix default for QEMU/KVM guests. see virt-install(1) also.
AC_SUBST([HWADDR_PREFIX],[54:52:00])

dnl libvirt networks (kept for reference).
AC_DEFINE_LIBVIRT_SIMPLE_NETWORK([1],[192.168.151],[virbr1],[net-1.local])
AC_DEFINE_LIBVIRT_SIMPLE_NETWORK([2],[192.168.152],[virbr2],[net-2.local])
AC_DEFINE_LIBVIRT_SIMPLE_NETWORK([3],[192.168.153],[virbr3],[net-3.local])
AC_SUBST([LIBVIRT_PRIMARY_NETWORK_BRIDGE],[virbr1])

dnl the server to provide kickstart tree, location and ks.cfg location
AC_DEFINE_KICKSTART([binaries],[http://master/contents],[http://master/ks])

dnl Installation key (since RHEL 5)
AC_DEFINE_RHEL_INSTALLATION_KEY([])

dnl ks password
AC_DEFINE_KICKSTART_PASSWORD([])

dnl http backend
dnl AC_HTTPD_BACKEND
httpd_backend="nginx"
AM_CONDITIONAL([USE_APACHE],[test x$httpd_backend = "xapache"])


AC_OUTPUT([
Makefile
miniascape.spec
aux/Makefile
aux/m4/Makefile
conf/Makefile
conf/fenced/Makefile
conf/fenced/fence_xvmd
conf/networks/Makefile
conf/networks/net-1.yaml
conf/networks/net-2.yaml
conf/networks/net-3.yaml
conf/kickstart/Makefile
conf/kickstart/apache/Makefile
conf/kickstart/apache/kickstart-dvd.conf
conf/kickstart/apache/kickstart.conf
conf/kickstart/nginx/Makefile
conf/kickstart/nginx/kickstart.conf
data/Makefile
data/kickstart/Makefile
data/kickstart/debian/Makefile
data/kickstart/debian/lenny-preseed.cfg
data/kickstart/rhel/Makefile
data/kickstart/rhel/rhel-6-0-i386-min.ks.cfg
data/kickstart/rhel/rhel-5-cluster.ks.cfg
data/kickstart/rhel/rhel-5-satellite.ks.cfg
data/kickstart/rhel/rhel-5-0-i386-min.ks.cfg
data/kickstart/rhel/rhel-4-0-i386-min.ks.cfg
data/kickstart/rhel/rhel-4-0-i386-default.ks.cfg
data/kickstart/rhel/rhel-3-0-i386-min.ks.cfg
data/kickstart/rhel/rhel-3-0-i386-default.ks.cfg
data/kickstart/rhel/rhel-3-2-i386-min.ks.cfg
data/kickstart/rhel/rhel-3-2-i386-default.ks.cfg
data/package/Makefile
data/package/data/Makefile
data/repackage/Makefile
data/templates/Makefile
data/templates/networks/Makefile
data/templates/networks/dnsmasq/Makefile
data/profiles/Makefile
data/profiles/rhel/Makefile
data/profiles/rhel/rhel-3-0-i386-min.cfg
rc/Makefile
rc/dnsmasq/Makefile
rc/dnsmasq/dnsmasq-net-1
rc/fenced/Makefile
src/Makefile
src/package.py
src/miniascape
src/net-register
src/net-unregister
tests/Makefile
tests/src/Makefile
tests/src/globals.py
])

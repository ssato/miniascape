AC_INIT([miniascape],[0.1.99])
AM_INIT_AUTOMAKE

AC_PROG_MKDIR_P
AC_PROG_QEMU_IMG
AC_PROG_RPMBUILD
AC_PATH_PROG([PYTHON],[python])
AC_PROG_VIRSH
AC_CHECK_SOURCE_ZIP

dnl FIXME: want to make it configurable
AC_SUBST([PACKAGEFILE_DIR],[/usr/share/miniascape])
AC_SUBST([REPACKAGEFILE_DIR],[/usr/share/miniascape/repackage])
AC_SUBST([ARCH],[noarch])

dnl hwaddr prefix default for QEMU/KVM guests. see virt-install(1) also.
AC_SUBST([HWADDR_PREFIX],[54:52:00])

dnl libvirt networks (kept for reference).
AC_DEFINE_LIBVIRT_SIMPLE_NETWORK([1],[192.168.51],[virbr1],[net-1.local])
AC_DEFINE_LIBVIRT_SIMPLE_NETWORK([2],[192.168.52],[virbr2],[net-2.local])
AC_DEFINE_LIBVIRT_SIMPLE_NETWORK([3],[192.168.53],[virbr3],[net-3.local])
AC_SUBST([LIBVIRT_PRIMARY_NETWORK_BRIDGE],[virbr1])

dnl the server to provide kickstart tree, location and ks.cfg location
AC_DEFINE_KICKSTART([binaries],[http://master/contents],[http://master/ks])

dnl Installation key (since RHEL 5)
AC_DEFINE_RHEL_INSTALLATION_KEY([])

dnl ks password
AC_DEFINE_KICKSTART_PASSWORD([])

dnl http backend
AC_HTTPD_BACKEND


AC_OUTPUT([
Makefile
miniascape.spec
data/Makefile
data/dnsmasq/Makefile
data/dnsmasq/miniascape-net-1
data/fenced/Makefile
data/fenced/init/Makefile
data/fenced/sysconfig/Makefile
data/fenced/sysconfig/fence_xvmd
data/libvirt/Makefile
data/libvirt/net-1.xml.in
data/libvirt/net-2.xml.in
data/libvirt/net-3.xml.in
data/kickstart/Makefile
data/kickstart/httpd/Makefile
data/kickstart/httpd/apache/Makefile
data/kickstart/httpd/apache/kickstart.conf
data/kickstart/httpd/apache/kickstart-dvd.conf
data/kickstart/httpd/nginx/Makefile
data/kickstart/httpd/nginx/kickstart.conf
data/kickstart/kscfgs/Makefile
data/kickstart/kscfgs/rhel/Makefile
data/kickstart/kscfgs/rhel/rhel-6-0-i386-min.ks.cfg
data/kickstart/kscfgs/rhel/rhel-5-cluster.ks.cfg
data/kickstart/kscfgs/rhel/rhel-5-satellite.ks.cfg
data/kickstart/kscfgs/rhel/rhel-5-0-i386-min.ks.cfg
data/kickstart/kscfgs/rhel/rhel-4-0-i386-min.ks.cfg
data/kickstart/kscfgs/rhel/rhel-4-0-i386-default.ks.cfg
data/kickstart/kscfgs/rhel/rhel-3-0-i386-min.ks.cfg
data/kickstart/kscfgs/rhel/rhel-3-0-i386-default.ks.cfg
data/kickstart/kscfgs/rhel/rhel-3-2-i386-min.ks.cfg
data/kickstart/kscfgs/rhel/rhel-3-2-i386-default.ks.cfg
data/package/Makefile
data/package/data/Makefile
data/repackage/Makefile
m4/Makefile
src/Makefile
src/package.py
src/tests/Makefile
])

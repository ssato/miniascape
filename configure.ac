AC_INIT([miniascape],[0.1.99])
AM_INIT_AUTOMAKE

AC_PROG_MKDIR_P
AC_PROG_QEMU_IMG
AC_PROG_RPMBUILD
AC_PATH_PROG([PYTHON],[python])
AC_PROG_VIRSH
AC_CHECK_SOURCE_ZIP

dnl FIXME: want to make it configurable
AC_SUBST([REPACKAGEFILE_DIR],[/usr/share/miniascape/repackage])

dnl hwaddr prefix default for QEMU/KVM guests. see virt-install(1) also.
hwaddr_prefix=54:52:00
AC_SUBST([HWADDR_PREFIX],[$hwaddr_prefix])

dnl libvirt networks (kept for reference).
AC_DEFINE_LIBVIRT_SIMPLE_NETWORK([1],[192.168.51],[virbr1],[net-1.local])
AC_DEFINE_LIBVIRT_SIMPLE_NETWORK([2],[192.168.52],[virbr2],[net-2.local])
AC_DEFINE_LIBVIRT_SIMPLE_NETWORK([3],[192.168.53],[virbr3],[net-3.local])
AC_SUBST([LIBVIRT_PRIMARY_NETWORK_BRIDGE],[virbr1])

dnl the server to provide kickstart tree, location and ks.cfg location
kstree_server=binaries
kstree_location="http://master/contents"
ks_location="http://master/ks"

AC_ARG_WITH([kstree_server],
  [AS_HELP_STRING([--with-kstree-server],[Kickstart tree server. default=$kstree_server])],
        [kstree_server=$withval])
AC_SUBST([KSTREE_SERVER],[$kstree_server])
AC_ARG_WITH([kstree_location],
  [AS_HELP_STRING([--with-kstree-location],[Kickstart tree location. default=$kstree_location])],
        [kstree_location=$withval])
AC_SUBST([KSTREE_LOCATION],[$kstree_location])

AC_ARG_WITH([ks_location],
  [AS_HELP_STRING([--with-ks-location],[Kickstart file location. default=$ks_location])],
        [ks_location=$withval])
AC_SUBST([KS_LOCATION],[$ks_location])


dnl Installation key (since RHEL 5)
rhel_installation_key=""
AC_ARG_WITH([rhel_installation_key],
  [AS_HELP_STRING([--with-rhel-installation-key],[RHEL Installation key])],
        [rhel_installation_key=$withval])
AC_SUBST([RHEL_INSTALLATION_KEY],[$rhel_installation_key])

dnl ks password
password=""
AC_ARG_WITH([password],
  [AS_HELP_STRING([--with-password],[Password for root in VMs.])],
        [password=$withval])
AC_SUBST([KS_PASSWORD],[$password])

dnl http backend
httpd_backend=nginx
enable_apache=false
AM_CONDITIONAL([ENABLE_APACHE], [test x$enable_apache = xtrue])


AC_OUTPUT([
Makefile
README
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
src/repackage.py
src/tests/Makefile
])

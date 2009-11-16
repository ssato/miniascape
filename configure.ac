AC_INIT([miniascape],[0.1])
AM_INIT_AUTOMAKE

AC_PROG_MKDIR_P
AC_PROG_QEMU_IMG

AC_PATH_PROG([PYTHON],[python])
AC_SUBST([VIRSH],[/usr/bin/virsh])

dnl FIXME: want to make it configurable
AC_SUBST([BUILDFILE_DIR],[/usr/share/miniascape/package])

dnl hwaddr prefix default for QEMU/KVM guests. see virt-install(1) also.
hwaddr_prefix=54:52:00
AC_SUBST([HWADDR_PREFIX],[$hwaddr_prefix])


dnl defaults:
net_1_bridge=virbr1
net_2_bridge=virbr2
net_3_bridge=virbr3
net_1_network=192.168.51
net_2_network=192.168.52
net_3_network=192.168.53
net_1_domain=net-1.local
net_2_domain=net-2.local
net_3_domain=net-3.local

AC_ARG_WITH([bridge1],
  [AS_HELP_STRING([--with-bridge1],[Bridge name for network 1. default=$net_1_bridge])],
    [net_1_bridge=$withval])
AC_ARG_WITH([net1],
  [AS_HELP_STRING([--with-net1],[Network address prefix for network 1. default=$net_1_network])],
    [net_1_network=$withval])
AC_ARG_WITH([domain1],
  [AS_HELP_STRING([--with-domain],[Domain name for network 1. default=$net_1_domain])],
    [net_1_domain=$withval])
AC_SUBST([NET_1_BRIDGE],[$net_1_bridge])
AC_SUBST([NET_1_NETWORK],[$net_1_network])
AC_SUBST([NET_1_DOMAIN],[$net_1_domain])

AC_ARG_WITH([bridge2],
  [AS_HELP_STRING([--with-bridge2],[Bridge name for network 2. default=$net_2_bridge])],
    [net_2_bridge=$withval])
AC_ARG_WITH([net2],
  [AS_HELP_STRING([--with-net2],[Network address prefix for network 2. default=$net_2_network])],
    [net_2_network=$withval])
AC_ARG_WITH([domain2],
  [AS_HELP_STRING([--with-domain],[Domain name for network 2. default=$net_2_domain])],
    [net_2_domain=$withval])
AC_SUBST([NET_2_BRIDGE],[$net_2_bridge])
AC_SUBST([NET_2_NETWORK],[$net_2_network])
AC_SUBST([NET_2_DOMAIN],[$net_2_domain])

AC_ARG_WITH([bridge3],
  [AS_HELP_STRING([--with-bridge3],[Bridge name for network 3. default=$net_3_bridge])],
    [net_3_bridge=$withval])
AC_ARG_WITH([net3],
  [AS_HELP_STRING([--with-net3],[Network address prefix for network 3. default=$net_3_network])],
    [net_3_network=$withval])
AC_ARG_WITH([domain3],
  [AS_HELP_STRING([--with-domain],[Domain name for network 3. default=$net_3_domain])],
    [net_3_domain=$withval])
AC_SUBST([NET_3_BRIDGE],[$net_3_bridge])
AC_SUBST([NET_3_NETWORK],[$net_3_network])
AC_SUBST([NET_3_DOMAIN],[$net_3_domain])

dnl reversed network address prefixes
AC_SUBST([NET_1_NETWORK_REVERSED],[`echo "$net_1_network" | sed 's/\([[^.]]*\).\([[^.]]*\).\([[^.]]*\)/\3.\2.\1/'`])
AC_SUBST([NET_2_NETWORK_REVERSED],[`echo "$net_2_network" | sed 's/\([[^.]]*\).\([[^.]]*\).\([[^.]]*\)/\3.\2.\1/'`])
AC_SUBST([NET_3_NETWORK_REVERSED],[`echo "$net_3_network" | sed 's/\([[^.]]*\).\([[^.]]*\).\([[^.]]*\)/\3.\2.\1/'`])

dnl interface which fence_xvmd listens on.
virt_network_interface=virbr1
AC_ARG_WITH([network-interface],
  [AS_HELP_STRING([--with-networ-interface],
    [Virt. network interaface which fence_xvmd will listen on. default=$virt_network_interface])],
      [virt_network_interface=$withval])
AC_SUBST([VIRT_NETWORK_INTERFACE],[$virt_network_interface])

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


AC_OUTPUT([
Makefile
README
TODO
miniascape.spec
data/Makefile
data/build/Makefile
data/package/Makefile
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
src/Makefile
src/repackage.py
src/tests/Makefile
])

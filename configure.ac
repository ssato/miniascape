AC_INIT([miniascape],[0.1])
AM_INIT_AUTOMAKE

AC_PROG_MKDIR_P
AC_PROG_QEMU_IMG

AC_PATH_PROG([PYTHON],[python])

AC_SUBST([VIRSH],[/usr/bin/virsh])
AC_SUBST([QEMU_IMG],[/usr/bin/qemu-img])

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
data/libvirt/Makefile
data/libvirt/net-1.xml.in
data/libvirt/net-2.xml.in
data/libvirt/net-3.xml.in
src/Makefile
src/repackage.py
src/tests/Makefile
])

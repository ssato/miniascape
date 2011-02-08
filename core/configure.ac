AC_INIT([miniascape],[0.1.20110207])
AM_INIT_AUTOMAKE([dist-xz foreign])

dnl http://www.flameeyes.eu/autotools-mythbuster/automake/silent.html
dnl It should better than using automake's silent-rules option to keep backward compatibility.
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])

AC_PROG_LN_S
AC_PROG_MKDIR_P
AC_PROG_SED

AC_PATH_PROG([VIRSH],[virsh])
AS_IF([test -z "$VIRSH"],[AC_MSG_ERROR([virsh is not found in your paths])])

AC_PATH_PROG([QEMU_IMG],[qemu-img])
AS_IF([test -z "$QEMU_IMG"],[AC_MSG_ERROR([qemu-img is not found in your paths])])

dnl hwaddr prefix default for QEMU/KVM guests. see virt-install(1) also.
hwaddr_prefix=54:52:00
AC_SUBST([HWADDR_PREFIX],[$hwaddr_prefix])


dnl defaults:
net_1_bridge=virbr1
net_2_bridge=virbr2
net_1_network=192.168.151
net_2_network=192.168.152
net_1_domain=net-1.local
net_2_domain=net-2.local

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

AC_SUBST([AUTOINST_CFG_URL_BASE],["http://$net_1_network.1/autoinst"])
AC_SUBST([AUTOINST_TREE_URL_BASE],["http://$net_1_network.1/contents"])

dnl hwaddr prefix default for QEMU/KVM guests. see virt-install(1) also.
AC_SUBST([HWADDR_PREFIX],[54:52:00])


dnl iscsi
iscsi_target_iqn="iqn.2009-08.local.master"
AC_ARG_WITH([iscsi-iqn],
  [AS_HELP_STRING([--with-iscsi-iqn],[iSCSI target IQN ID. default=$iscsi_target_iqn])],
    [iscsi_target_iqn=$withval])
AC_SUBST([ISCSI_TARGET_IQN],[$iscsi_target_iqn])


dnl which to use for web service?
AS_IF([test -f /etc/fedora-release],[nginx=true],[nginx=false])
AC_ARG_ENABLE([nginx],
     [  --enable-nginx  Use nginx instead of apache httpd],
     [case "${enableval}" in
       yes) nginx=true ;;
       no)  nginx=false ;;
       *) AC_MSG_ERROR([bad value ${enableval} for --enable-nginx]) ;;
     esac],[nginx=$nginx])
AM_CONDITIONAL([USE_NGINX],[test x$nginx = xtrue])


AC_CONFIG_FILES([
Makefile
config
miniascape.spec
devel/Makefile
devel/vars.mk
devel/rpm.mk
devel/vm.spec.in
services/Makefile
services/iptables/Makefile
services/iptables/iptables.rules
services/iscsi/Makefile
services/iscsi/tid-xx-sample.conf
services/networks/Makefile
services/networks/net-1.xml
services/networks/net-2.xml
services/www/Makefile
services/nfs/Makefile
tools/Makefile
vm/Makefile
vm/autoinstall/Makefile
vm/autoinstall/fedora-13-i386-min.ks.cfg
vm/autoinstall/fedora-14-i386-min.ks.cfg
vm/autoinstall/rhel-6-0-i386-min.ks.cfg
vm/autoinstall/rhel-5-cluster.ks.cfg
vm/autoinstall/rhel-5-satellite.ks.cfg
vm/autoinstall/rhel-5-mrg.ks.cfg
vm/autoinstall/rhel-5-jboss.ks.cfg
vm/autoinstall/rhel-5-luci.ks.cfg
vm/autoinstall/rhel-5-0-i386-min.ks.cfg
vm/autoinstall/rhel-4-0-i386-min.ks.cfg
vm/autoinstall/rhel-4-0-i386-default.ks.cfg
vm/autoinstall/rhel-3-0-i386-min.ks.cfg
vm/autoinstall/rhel-3-0-i386-default.ks.cfg
vm/autoinstall/rhel-3-2-i386-min.ks.cfg
vm/autoinstall/rhel-3-2-i386-default.ks.cfg
vm/profiles/Makefile
vm/profiles/site.cfg
vm/profiles/vm.d/Makefile
])

AC_OUTPUT

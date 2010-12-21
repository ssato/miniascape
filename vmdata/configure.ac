AC_INIT([miniascape-vmdata],[0.1.20101221])
dnl AM_INIT_AUTOMAKE([1.11 silent-rules foreign])
AM_INIT_AUTOMAKE([silent-rules foreign])

dnl http://www.flameeyes.eu/autotools-mythbuster/automake/silent.html
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])

AC_PROG_SED


dnl
dnl I decided to fixed the following parameters and make them not configurable.
dnl
dnl These are originally defined in ../core/configure.ac and must be changed
dnl if these are customized in the core 'miniascape' package.
dnl
net_1_prefix=192.168.151
net_2_prefix=192.168.152
net_3_prefix=192.168.153
net_1_domain=net-1.local
net_2_domain=net-2.local
net_3_domain=net-3.local
net_gateway=$net_1_prefix.1
install_server="$net_gateway"
hwaddr_prefix=54:52:00

AC_SUBST([NET_1_PREFIX],[$net_1_prefix])
AC_SUBST([NET_2_PREFIX],[$net_2_prefix])
AC_SUBST([NET_3_PREFIX],[$net_3_prefix])
AC_SUBST([NET_1_DOMAIN],[$net_1_domain])
AC_SUBST([NET_2_DOMAIN],[$net_2_domain])
AC_SUBST([NET_3_DOMAIN],[$net_3_domain])

AC_SUBST([BASE_PACKAGE],[miniascape])

AC_SUBST([AUTOINST_CFG_URL_BASE],["http://$install_server/autoinst"])
AC_SUBST([AUTOINST_TREE_URL_BASE],["http://$install_server/contents"])

dnl hwaddr prefix default for QEMU/KVM guests. see virt-install(1) also.
AC_SUBST([HWADDR_PREFIX],[$hwaddr_prefix])


AC_CONFIG_FILES([
Makefile
miniascape-vmdata.spec
autoinstall/Makefile
autoinstall/fedora-13-i386-min.ks.cfg
autoinstall/fedora-14-i386-min.ks.cfg
autoinstall/rhel-6-0-i386-min.ks.cfg
autoinstall/rhel-5-cluster.ks.cfg
autoinstall/rhel-5-satellite.ks.cfg
autoinstall/rhel-5-mrg.ks.cfg
autoinstall/rhel-5-jboss.ks.cfg
autoinstall/rhel-5-luci.ks.cfg
autoinstall/rhel-5-0-i386-min.ks.cfg
autoinstall/rhel-4-0-i386-min.ks.cfg
autoinstall/rhel-4-0-i386-default.ks.cfg
autoinstall/rhel-3-0-i386-min.ks.cfg
autoinstall/rhel-3-0-i386-default.ks.cfg
autoinstall/rhel-3-2-i386-min.ks.cfg
autoinstall/rhel-3-2-i386-default.ks.cfg
profiles/Makefile
profiles/site.cfg
])

AC_OUTPUT

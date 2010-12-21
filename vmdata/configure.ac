AC_INIT([miniascape-vmdata],[0.1.99])
AM_INIT_AUTOMAKE([foreign])

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
profiles/rhel-3-0-guest-1.cfg
profiles/rhel-3-1-guest-1.cfg
profiles/rhel-3-2-guest-1.cfg
profiles/rhel-3-3-guest-1.cfg
profiles/rhel-3-4-guest-1.cfg
profiles/rhel-3-5-guest-1.cfg
profiles/rhel-3-6-guest-1.cfg
profiles/rhel-3-7-guest-1.cfg
profiles/rhel-3-8-guest-1.cfg
profiles/rhel-3-9-guest-1.cfg
profiles/rhel-4-0-guest-1.cfg
profiles/rhel-4-1-guest-1.cfg
profiles/rhel-4-2-guest-1.cfg
profiles/rhel-4-3-guest-1.cfg
profiles/rhel-4-4-guest-1.cfg
profiles/rhel-4-5-guest-1.cfg
profiles/rhel-4-6-guest-1.cfg
profiles/rhel-4-7-guest-1.cfg
profiles/rhel-4-8-guest-1.cfg
profiles/rhel-5-0-guest-1.cfg
profiles/rhel-5-1-guest-1.cfg
profiles/rhel-5-2-guest-1.cfg
profiles/rhel-5-3-guest-1.cfg
profiles/rhel-5-4-guest-1.cfg
profiles/rhel-5-5-guest-1.cfg
profiles/rhel-5-cluster-1.cfg
profiles/rhel-5-cluster-2.cfg
profiles/rhel-5-cluster-3.cfg
profiles/rhel-5-cluster-4.cfg
profiles/rhel-5-cluster-5.cfg
profiles/rhel-5-luci-0.cfg
profiles/rhel-6-0-guest-1.cfg
])

AC_OUTPUT

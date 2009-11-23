#
# m4 macros for python-virtinst (virt-install)
#
# Copyright (c) 2009 Satoru SATOH <satoru.satoh@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
#
# As a special exception, the respective Autoconf Macro's copyright owner
# gives unlimited permission to copy, distribute and modify the configure
# scripts that are the output of Autoconf when processing the Macro. You
# need not follow the terms of the GNU General Public License when using
# or distributing such scripts, even though portions of the text of the
# Macro appear in them. The GNU General Public License (GPL) does govern
# all other use of the material that constitutes the Autoconf Macro.
#
# This special exception to the GPL applies to versions of the Autoconf
# Macro released by the Autoconf Macro Archive. When you make and
# distribute a modified version of the Autoconf Macro, you may extend this
# special exception to the GPL to apply to your modified version as well.
#

#
# AC_PROG_VIRTINST - check if virt-install is available.
#
AC_DEFUN([AC_PROG_VIRTINST],[
    AC_PATH_PROG([VIRTINST],[virt-install],[])
    AS_IF([test "x$VIRTINST" = "x"],
        [AC_MSG_ERROR([virt-install is not found in your PATH])],
        [AC_SUBST([VIRTINST],[$VIRTINST])])
])


#
# AX_VIRT_DOMAIN_OPTIONS
#
# Configure virt domain profile passed to virt-install's options lator.
#
AC_DEFUN([AX_VIRT_DOMAIN_OPTIONS],[
    AC_REQUIRE([AC_PROG_VIRTINST])

    dnl set defaults if empty.
    dnl TODO: How to specify those before/when this macro called.
    AS_IF([test -z "$ax_virt_connect"],[connect="qemu:///system"],[])
    AS_IF([test -z "$ax_virt_domain_memory"],[domain_memory=256],[])
    AS_IF([test -z "$ax_virt_domain_arch"],[domain_arch=i686],[])
    AS_IF([test -z "$ax_virt_domain_vcpus"],[domain_vcpus=1],[])
    AS_IF([test -z "$ax_virt_domain_cpuset"],[domain_cpuset=auto],[])
    AS_IF([test -z "$ax_virt_domain_keymap"],[domain_keymap=en-US],[])
    AS_IF([test -z "$ax_virt_domain_disk_size"],[domain_disk_size=5],[])
    AS_IF([test -z "$ax_virt_domain_disk_bus"],[domain_disk_bus=ide],[])
    AS_IF([test -z "$ax_virt_domain_disk_perms"],[domain_disk_perms=rw],[])
    AS_IF([test -z "$ax_virt_domain_disk_format"],[domain_disk_format=qcow2],[])
    AS_IF([test -z "$ax_virt_domain_networks"],[domain_networks=""],[])
    AS_IF([test -z "$ax_virt_domain_install_tree"],[domain_install_tree=""],[])
    AS_IF([test -z "$ax_virt_domain_install_extras"],[domain_install_extras=""],[])
    AS_IF([test -z "$ax_virt_domain_os_variant"],[domain_os_variant="rhel5"],[])
    AS_IF([test -z "$ax_virt_virtinst_wait"],[virtinst_wait=20],[])

    dnl TODO: support xen and qemu:///session.
    AC_ARG_WITH([connect],
        [AS_HELP_STRING([--with-connect],
            [Hypervisor connection. @<:@default="$connect"@:>@])],
        [connect="$withval"],[])
    AC_SUBST([CONNECT],["$connect"])

    AC_ARG_WITH([domain-memory],
        [AS_HELP_STRING([--with-domain-memory],
            [Domain RAM size in kbyte. @<:@default="$domain_memory"@:>@])],
        [domain_memory="$withval"],[])
    AC_SUBST([DOMAIN_MEMORY],["$domain_memory"])

    AC_ARG_WITH([domain-arch],
        [AS_HELP_STRING([--with-domain-arch],
            [Domain arch. @<:@default="$domain_arch"@:>@])],
        [domain_arch="$withval"],[])
    AC_SUBST([DOMAIN_ARCH],["$domain_arch"])

    AC_ARG_WITH([domain-vcpus],
        [AS_HELP_STRING([--with-domain-vcpus],
            [Domain number of CPUs. @<:@default="$domain_vcpus"@:>@])],
        [domain_vcpus="$withval"],[])
    AC_SUBST([DOMAIN_VCPUS],["$domain_vcpus"])

    AC_ARG_WITH([domain-cpuset],
        [AS_HELP_STRING([--with-domain-cpuset],
            [Domain CPU set. @<:@default="$domain_cpuset"@:>@])],
        [domain_cpuset="$withval"],[])
    AC_SUBST([DOMAIN_CPUSET],["$domain_cpuset"])

    AC_ARG_WITH([domain-keymap],
        [AS_HELP_STRING([--with-domain-keymap],
            [Domain keymap. @<:@default="$domain_keymap"@:>@])],
        [domain_keymap="$withval"],[])
    AC_SUBST([DOMAIN_KEYMAP],["$domain_keymap"])

    AC_ARG_WITH([domain-disk-size],
        [AS_HELP_STRING([--with-domain-disk-size],
            [Domain disk size in GByte. @<:@default="$domain_disk_size"@:>@])],
        [domain_disk_size="$withval"],[])
    AC_SUBST([DOMAIN_DISK_SIZE],["$domain_disk_size"])

    AC_ARG_WITH([domain-disk-bus],
        [AS_HELP_STRING([--with-domain-disk-bus],
            [Domain disk bus type. @<:@default="$domain_disk_bus"@:>@])],
        [domain_disk_bus="$withval"],[])
    AC_SUBST([DOMAIN_DISK_BUS],["$domain_disk_bus"])

    AC_ARG_WITH([domain-disk-perms],
        [AS_HELP_STRING([--with-domain-disk-perms],
            [Domain disk permission type; rw/ro/sh. @<:@default="$domain_disk_perms"@:>@])],
        [domain_disk_perms="$withval"],[])
    AC_SUBST([DOMAIN_DISK_PERMS],["$domain_disk_perms"])

    AC_ARG_WITH([domain-disk-format],
        [AS_HELP_STRING([--with-domain-disk-format],
            [Domain disk format type. @<:@default="$domain_disk_format"@:>@])],
        [domain_disk_format="$withval"],[])
    AC_SUBST([DOMAIN_DISK_FORMAT],["$domain_disk_format"])

    dnl TODO: How to specify multiple networs and mac addresses at once.
    AC_ARG_WITH([domain-networks],
        [AS_HELP_STRING([--with-domain-networks],
            [Domain networks. ";" separated list of comma separated network and mac, e.g. network:net-1,aa:bb:cc:00:00:01;network:net-2,aa:bb:cc:00:00:02. @<:@default="$domain_networks"@:>@])],
        [domain_networks="$withval"],[])
    AS_IF([test -n "$domain_networks"],
        [network_opts="--network="`echo $domain_networks | sed "s/;/ --network=/g; s/,/ --mac=/g"`],
        [network_opts="--nonetworks"])
    AC_SUBST([VIRTINST_NETWORK_OPTS],[$network_opts])
    AC_SUBST([DOMAIN_NETWORKS],["$domain_networks"])

    AC_ARG_WITH([domain-install-tree],
        [AS_HELP_STRING([--with-domain-install-tree],
            [Domain installation tree location. @<:@default="$domain_install_tree"@:>@])],
        [domain_install_tree="$withval"],[])
    AC_SUBST([DOMAIN_INSTALL_TREE],["$domain_install_tree"])

    AC_ARG_WITH([domain-install-extras],
        [AS_HELP_STRING([--with-domain-install-extras],
            [Domain installation extra args. @<:@default="$domain_install_extras"@:>@])],
        [domain_install_extras="$withval"],[])
    AC_SUBST([DOMAIN_INSTALL_EXTRA_ARGS],["$domain_install_extras"])

    AC_ARG_WITH([domain-os-variant],
        [AS_HELP_STRING([--with-domain-os-variant],
            [Domain os variant. @<:@default="$domain_os_variant"@:>@])],
        [domain_os_variant="$withval"],[])
    AC_SUBST([DOMAIN_OS_VARIANT],["$domain_os_variant"])

    AC_ARG_WITH([virtinst-wait],
        [AS_HELP_STRING([--with-virtinst-wait],
            [Wait to complete installation in minutes. @<:@default="$virtinst_wait"@:>@])],
        [virtinst_wait="$withval"],[])
    AC_SUBST([VIRTINST_WAIT],["$virtinst_wait"])

])

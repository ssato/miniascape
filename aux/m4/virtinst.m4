#
# m4 macros for python-virtinst (virt-install)
#
# Copyright (c) 2009 Satoru SATOH <satoru.satoh@gmail.com>
#
# License: see the note in REAMDE[.in] file at the top directory.
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
# AC_WITH_VIRTINST_SPEC ([SPEC]) - Set virt-install options for domain.
#
AC_DEFUN([AC_WITH_VIRTINST_SPEC],[
    AC_REQUIRE([AC_PROG_VIRTINST])

    AS_IF([test -n "$1"],[specfile=$1],[specfile=domain-profile.sh])

    dnl AC_ARG_WITH([virtinst-spec],
    dnl     [AS_HELP_STRING([--with-virtinst-spec=SPEC_FILE],
    dnl         [Spec file path to set virtinst options. @<:@default="$specfile"@:>@])],
    dnl     [specfile="$withval"])

    AS_IF([test -f $specfile],[. $specfile],[AC_MSG_ERROR([Could not load $specfile])])

    AS_IF([test "x$CONNECT" = "x"],[CONNECT="qemu:///system"],[])
    AS_IF([test "x$DOMAIN_MEMORY" = "x"],[DOMAIN_MEMORY=256],[])
    AS_IF([test "x$DOMAIN_ARCH" = "x"],[DOMAIN_ARCH=i686],[])
    AS_IF([test "x$DOMAIN_VCPUS" = "x"],[DOMAIN_VCPUS=1],[])
    AS_IF([test "x$DOMAIN_CPUSET" = "x"],[DOMAIN_CPUSET=auto],[])
    AS_IF([test "x$DOMAIN_KEYMAP" = "x"],[DOMAIN_KEYMAP=en-US],[])
    AS_IF([test "x$DOMAIN_OS_VARIANT" = "x"],[DOMAIN_OS_VARIANT="rhel5"],[])
    AS_IF([test "x$VIRTINST_WAIT" = "x"],[VIRTINST_WAIT=20],[])

    AS_IF([test "x$DOMAIN_DISK_1_SIZE" = "x"],[DOMAIN_DISK_1_SIZE=5],[])
    AS_IF([test "x$DOMAIN_DISK_1_BUS" = "x"],[DOMAIN_DISK_1_BUS=ide],[])
    AS_IF([test "x$DOMAIN_DISK_1_PERMS" = "x"],[DOMAIN_DISK_1_PERMS=rw],[])
    AS_IF([test "x$DOMAIN_DISK_1_FORMAT" = "x"],[DOMAIN_DISK_1_FORMAT=qcow2],[])

    AS_IF([test "x$DOMAIN_NETWORK_1" = "x"],[DOMAIN_NETWORK_1=network:net-1],[])
    AS_IF([test "x$DOMAIN_NETWORK_2" = "x"],[DOMAIN_NETWORK_2=network:net-1],[])
    AS_IF([test "x$DOMAIN_NETWORK_3" = "x"],[DOMAIN_NETWORK_3=network:net-3],[])
    AS_IF([test "x$DOMAIN_NETWORK_4" = "x"],[DOMAIN_NETWORK_4=network:net-3],[])
    AS_IF([test "x$DOMAIN_NETWORK_1_MAC" = "x"],
        [DOMAIN_NETWORK_1_MAC=`python -c "from virtinst.util import randomMAC; print randomMAC('qemu')"`],[])
    AS_IF([test "x$DOMAIN_NETWORK_2_MAC" = "x"],
        [DOMAIN_NETWORK_2_MAC=`python -c "from virtinst.util import randomMAC; print randomMAC('qemu')"`],[])
    AS_IF([test "x$DOMAIN_NETWORK_3_MAC" = "x"],
        [DOMAIN_NETWORK_3_MAC=`python -c "from virtinst.util import randomMAC; print randomMAC('qemu')"`],[])
    AS_IF([test "x$DOMAIN_NETWORK_4_MAC" = "x"],
        [DOMAIN_NETWORK_4_MAC=`python -c "from virtinst.util import randomMAC; print randomMAC('qemu')"`],[])

    AS_IF([test "x$DOMAIN_INSTALL_SOURCE" = "x"],[AC_MSG_ERROR([DOMAIN_INSTALL_SOURCE must be set]),[])
    AS_IF([test "x$DOMAIN_INSTALL_EXTRA_ARGS" = "x"],[AC_MSG_ERROR([DOMAIN_INSTALL_EXTRA_ARGS must be set]),[])

    AC_SUBST([CONNECT],[$CONNECT])
    AC_SUBST([DOMAIN_MEMORY],[$DOMAIN_MEMORY])
    AC_SUBST([DOMAIN_ARCH],[$DOMAIN_ARCH])
    AC_SUBST([DOMAIN_VCPUS],[$DOMAIN_VCPUS])
    AC_SUBST([DOMAIN_CPUSET],[$DOMAIN_CPUSET])
    AC_SUBST([DOMAIN_KEYMAP],[$DOMAIN_KEYMAP])
    AC_SUBST([DOMAIN_OS_VARIANT],[$DOMAIN_OS_VARIANT])
    AC_SUBST([VIRTINST_WAIT],[$VIRTINST_WAIT])

    AC_SUBST([DOMAIN_DISK_1_SIZE],[$DOMAIN_DISK_1_SIZE])
    AC_SUBST([DOMAIN_DISK_1_BUS],[$DOMAIN_DISK_1_BUS])
    AC_SUBST([DOMAIN_DISK_1_PERMS],[$DOMAIN_DISK_1_PERMS])
    AC_SUBST([DOMAIN_DISK_1_FORMAT],[$DOMAIN_DISK_1_FORMAT])

    AC_SUBST([DOMAIN_NETWORK_1],[$DOMAIN_NETWORK_1])
    AC_SUBST([DOMAIN_NETWORK_2],[$DOMAIN_NETWORK_2])
    AC_SUBST([DOMAIN_NETWORK_3],[$DOMAIN_NETWORK_3])
    AC_SUBST([DOMAIN_NETWORK_4],[$DOMAIN_NETWORK_4])
    AC_SUBST([DOMAIN_NETWORK_1_MAC],[$DOMAIN_NETWORK_1_MAC])
    AC_SUBST([DOMAIN_NETWORK_2_MAC],[$DOMAIN_NETWORK_2_MAC])
    AC_SUBST([DOMAIN_NETWORK_3_MAC],[$DOMAIN_NETWORK_3_MAC])
    AC_SUBST([DOMAIN_NETWORK_4_MAC],[$DOMAIN_NETWORK_4_MAC])

    AC_SUBST([DOMAIN_INSTALL_SOURCE],[$DOMAIN_INSTALL_SOURCE])
    AC_SUBST([DOMAIN_INSTALL_EXTRA_ARGS],[$DOMAIN_INSTALL_EXTRA_ARGS])
])

#
# AC_VIRTINST_DOMAIN_DISK_OPTIONS (DISK-INDEX)
#
# Configure virt domain disk profile passed to virt-install's options lator.
#
AC_DEFUN([AC_VIRTINST_DOMAIN_DISK_OPTIONS],[
    domain_disk_size=5
    domain_disk_bus=ide
    domain_disk_perms=rw
    domain_disk_format=qcow2

    AC_ARG_WITH([domain-disk-$1-size],
        [AS_HELP_STRING([--with-domain-disk-$1-size],
            [Domain disk size in GByte. @<:@default="$domain_disk_size"@:>@])],
        [domain_disk_size="$withval"],[])
    AC_SUBST([DOMAIN_DISK_$1_SIZE],["$domain_disk_size"])

    AC_ARG_WITH([domain-disk-$1-bus],
        [AS_HELP_STRING([--with-domain-disk-$1-bus],
            [Domain disk bus type. @<:@default="$domain_disk_bus"@:>@])],
        [domain_disk_bus="$withval"],[])
    AC_SUBST([DOMAIN_DISK_$1_BUS],["$domain_disk_bus"])

    AC_ARG_WITH([domain-disk-$1-perms],
        [AS_HELP_STRING([--with-domain-disk-$1-perms],
            [Domain disk permission type; rw/ro/sh. @<:@default="$domain_disk_perms"@:>@])],
        [domain_disk_perms="$withval"],[])
    AC_SUBST([DOMAIN_DISK_$1_PERMS],["$domain_disk_perms"])

    AC_ARG_WITH([domain-disk-$1-format],
        [AS_HELP_STRING([--with-domain-disk-$1-format],
            [Domain disk format type. @<:@default="$domain_disk_format"@:>@])],
        [domain_disk_format="$withval"],[])
    AC_SUBST([DOMAIN_DISK_$1_FORMAT],["$domain_disk_format"])
])

#
# AC_VIRTINST_DOMAIN_NETWORK_OPTIONS (NET-INDEX, NETWORK, MAC)
#
# Configure virt domain network profile passed to virt-install's options lator.
#
AC_DEFUN([AC_VIRTINST_DOMAIN_NETWORK_OPTIONS],[
    dnl AC_REQUIRE([AC_PROG_VIRTINST])

    dnl FIXME: what should be done if python and python-virtinst is not installed.
    AS_IF([test -n "$2"],[domain_network=$2],[domain_network=network:default])
    AS_IF([test -n "$3"],[domain_network_mac=$3],
        [domain_network_mac=`python -c "from virtinst.util import randomMAC; print randomMAC('qemu')"`])

    AC_ARG_WITH([domain-network-$1],
        [AS_HELP_STRING([--with-domain-network-$1],
            [Domain network. @<:@default="$domain_network"@:>@])],
        [domain_network="$withval"],[])
    AC_SUBST([DOMAIN_NETWORK_$1],["$domain_network"])

    AC_ARG_WITH([domain-network-$1-mac],
        [AS_HELP_STRING([--with-domain-network-$1-mac],
            [Domain network. @<:@default="$domain_network_mac"@:>@])],
        [domain_network_mac="$withval"],[])
    AC_SUBST([DOMAIN_NETWORK_$1_MAC],["$domain_network_mac"])
])

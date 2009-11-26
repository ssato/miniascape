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
# AC_VIRTINST_DOMAIN_OPTIONS
#
# Configure virt domain profile passed to virt-install's options lator.
#
AC_DEFUN([AC_VIRTINST_DOMAIN_OPTIONS],[
    AC_REQUIRE([AC_PROG_VIRTINST])

    connect="qemu:///system"
    domain_memory=256
    domain_arch=i686
    domain_vcpus=1
    domain_cpuset=auto
    domain_keymap=en-US
    domain_os_variant="rhel5"
    virtinst_wait=20

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

#
# AC_VIRTINST_DOMAIN_INSTALL_OPTIONS (INSTALL-SOURCE, INSTALL-EXTRAS)
#
# Configure virt domain installatin options passed to virt-install.
#
AC_DEFUN([AC_VIRTINST_DOMAIN_INSTALL_OPTIONS],[
    domain_install_source=$1
    domain_install_extras=$2

    AC_ARG_WITH([domain-install-source],
        [AS_HELP_STRING([--with-domain-install-source],
            [Domain installation source location. @<:@default="$domain_install_source"@:>@])],
        [domain_install_source="$withval"],[])
    AC_SUBST([DOMAIN_INSTALL_SOURCE],["$domain_install_source"])

    AC_ARG_WITH([domain-install-extras],
        [AS_HELP_STRING([--with-domain-install-extras],
            [Domain installation extra args. @<:@default="$domain_install_extras"@:>@])],
        [domain_install_extras="$withval"],[])
    AC_SUBST([DOMAIN_INSTALL_EXTRA_ARGS],["$domain_install_extras"])
])


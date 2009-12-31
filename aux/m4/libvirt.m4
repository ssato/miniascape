#
# m4 macros for libvirt and virsh
#
# Copyright (c) 2009 Satoru SATOH <satoru.satoh at gmail.com>
#
# License: see the note in REAMDE[.in] file at the top directory.
#

#
# AC_PROG_LIBVIRTD - check if libvirt[d] is installed
#
AC_DEFUN([AC_PROG_LIBVIRTD],[
    AC_PATH_PROG([LIBVIRTD],[libvirtd],[],
        [/usr/sbin$PATH_SEPARATOR/usr/local/sbin])
    AS_IF([test "x$LIBVIRTD" = "x"],
        [AC_MSG_ERROR([libvirtd is not found in /usr/sbin nor /usr/local/sbin.])],[])
])

#
# AC_PROG_SERVICE_LIBVIRTD
# - check if libvirtd service is installed
#
AC_DEFUN([AC_PROG_SERVICE_LIBVIRTD],[
    dnl AC_REQUIRE([AC_PROG_LIBVIRTD])

    AC_PATH_PROG([SERVICE_LIBVIRTD],[libvirtd],[],
        [/etc/rc.d/init.d$PATH_SEPARATOR/etc/init.d$PATH_SEPARATOR/usr/local/etc/init.d])
    AS_IF([test "x$SERVICE_LIBVIRTD" = "x"],
        [AC_MSG_ERROR([service libvirtd is not found.])],[])
])

#
# AC_CHECK_SERVICE_LIBVIRTD_RUNNING - check if libvirtd service is running
#
AC_DEFUN([AC_CHECK_SERVICE_LIBVIRTD_RUNNING],[
    AC_REQUIRE([AC_PROG_SERVICE_LIBVIRTD])

    AC_MSG_CHECKING([whether the service libvirtd is running])
    is_running="no"

    AS_IF([$SERVICE_LIBVIRTD status > /dev/null 2> /dev/null],
        [AC_MSG_RESULT([yes])],
        [AC_MSG_ERROR([service libvirtd is not running.])])
])

#
# AC_PROG_VIRSH - check if virsh is installed along with libvirt.
#
AC_DEFUN([AC_PROG_VIRSH],[
    AC_PATH_PROG([VIRSH],[virsh],[])
    AS_IF([test "x$VIRSH" = "x"],
        [AC_MSG_ERROR([virsh is not found in your PATH])],
        [AC_SUBST([VIRSH],[$VIRSH])])
])

#
# AC_CHECK_DOMAIN_NEW (DOMAIN-NAME) - check if given domain does not exist.
#
AC_DEFUN([AC_CHECK_DOMAIN_NEW],[
    AC_REQUIRE([AC_PROG_VIRSH])

    AC_MSG_CHECKING([whether the domain '$1' is new])
    AS_IF([$VIRSH domid $1 > /dev/null 2> /dev/null],
        [AC_MSG_ERROR(Domain $1 already exists)],
        [AC_MSG_RESULT([yes])])
])

#
# AC_DEFINE_LIBVIRT_SIMPLE_NETWORK (INDEX, ADDRESS-BASE, BRIDGE, DOMAIN)
# - configure parameters for simple libvirt network
#
# ex. AC_DEFINE_LIBVIRT_SIMPLE_NETWORK([1],[192.168.51],[virbr1],[net-1.local])
#
# FIXME: ugly.
#
AC_DEFUN([AC_DEFINE_LIBVIRT_SIMPLE_NETWORK],[
    libvirt_network_index=$1
    libvirt_network_base=$2
    libvirt_network_bridge=$3
    libvirt_network_domain=$4

    AC_ARG_WITH([network-$1],
        [AS_HELP_STRING([--with-network-$1],
            [Base address for the network $1. @<:@default="$2"@:>@])],
        [AC_SUBST([LIBVIRT_NETWORK_$1_BASE],[$withval])],
        [AC_SUBST([LIBVIRT_NETWORK_$1_BASE],[$2])])

    AC_ARG_WITH([network-$1-bridge],
        [AS_HELP_STRING([--with-network-$1-bridge],
            [Bridge name for the network $1. @<:@default="$3"@:>@])],
        [AC_SUBST([LIBVIRT_NETWORK_$1_BRIDGE],[$withval])],
        [AC_SUBST([LIBVIRT_NETWORK_$1_BRIDGE],[$3])])

    AC_ARG_WITH([network-$1-domain],
        [AS_HELP_STRING([--with-network-$1-domain],
            [Domain name for the network $1. @<:@default="$4"@:>@])],
        [AC_SUBST([LIBVIRT_NETWORK_$1_DOMAIN],[$withval])],
        [AC_SUBST([LIBVIRT_NETWORK_$1_DOMAIN],[$4])])

    AC_SUBST([LIBVIRT_NETWORK_$1_REVERSED],[`echo "$2" | sed 's/\([[^.]]*\).\([[^.]]*\).\([[^.]]*\)/\3.\2.\1/'`])
])

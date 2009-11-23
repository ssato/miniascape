#
# libvirt, virsh and virt-install related m4 macros
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


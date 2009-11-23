#
# qemu and kvm related m4 macros
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
# AC_PROG_QEMU[_KVM]
# - check if qemu[-kvm] is installed and set its path to QEMU.
#
AC_DEFUN([AC_PROG_QEMU],[
    AC_PATH_PROG([QEMU],[qemu],[])
    AS_IF([test "x$QEMU" = "x"],
        [AC_MSG_ERROR([qemu is not found in your PATH])],
        [AC_SUBST([QEMU],[$QEMU])])
])

AC_DEFUN([AC_PROG_QEMU_KVM],[
    AC_PATH_PROG([QEMU],[qemu-kvm],[])
    AS_IF([test "x$QEMU" = "x"],
        [AC_MSG_ERROR([qemu-kvm is not found in your PATH])],
        [AC_SUBST([QEMU],[$QEMU])])
])

#
# AC_PROG_QEMU_IMG
# - check if qemu-img used for disk image creation and conversion is installed.
AC_DEFUN([AC_PROG_QEMU_IMG],[
    AC_PATH_PROG([QEMU_IMG],[qemu-img],[])
    AS_IF([test "x$QEMU_IMG" = "x"],
        [AC_MSG_ERROR([qemu-img is not found in your PATH])],
        [AC_SUBST([QEMU_IMG],[$QEMU_IMG])])
])

#
# AC_CHECK_KVM_DEVICE - check if kvm (/dev/kvm) is available.
#
AC_DEFUN([AC_CHECK_KVM_DEVICE],[
    dnl AC_REQUIRE([AC_PROG_QEMU_KVM])

    AC_MSG_CHECKING([whether /dev/kvm exists])
    AS_IF([test -e /dev/kvm && test -c /dev/kvm > /dev/null 2> /dev/null],
        [AC_MSG_RESULT([yes])],
        [AC_MSG_ERROR([no. Check the processor and BIOS configuration of your system.])])
])

dnl vim: set sw=4 ts=4 et:

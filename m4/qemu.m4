#
# qemu related m4 macros
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
# AC_PROG_QEMU - check if qemu is installed
#
AC_DEFUN([AC_PROG_QEMU],[AC_PATH_PROG([QEMU],[qemu])])


#
# AC_PROG_KVM - check if qemu-kvm is installed and works
#
AC_DEFUN([AC_PROG_KVM],[
  AC_REQUIRE([AC_PROG_QEMU])

  AC_PATH_PROG([KVM],[qemu-kvm])

  dnl TODO: check /dev/kvm only if qemu-kvm is found.
  AS_IF([test "$KVM+set" = "set"],
        [
          AC_MSG_WARN(qemu-kvm is not found. much slower qemu will be used instead.)dnl
          AC_SUBST([HAVE_QEMU_KVM],["no"])dnl
        ],[
          AC_SUBST([HAVE_QEMU_KVM],["yes"])
          AC_CHECK_FILE([/dev/kvm],[],
            [AC_MSG_ERROR(qemu-kvm is found but your system does not support it. Check the related configuration such as BIOS.)])
        ])
])


#
# AC_PROG_QEMU_IMG - check if qemu-img used for disk image creation and
#                    conversion is installed.
AC_DEFUN([AC_PROG_QEMU_IMG],[AC_PATH_PROG([QEMU_IMG],[qemu-img])])


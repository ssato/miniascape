#
# qemu and kvm related m4 macros
#
# Copyright (c) 2009 Satoru SATOH <satoru.satoh@gmail.com>
#
# License: see the note in REAMDE[.in] file at the top directory.
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

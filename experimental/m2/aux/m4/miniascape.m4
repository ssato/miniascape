#
# m4 macros for miniascape
#
# Copyright (c) 2010 Satoru SATOH <satoru.satoh at gmail.com>
#
# License: MIT
#

#
# AC_PROG_MINIASCAPE - check if miniascape is installed and available
#
AC_DEFUN([AC_PROG_MINIASCAPE],[
    AC_PATH_PROG([MINIASCAPE],[miniascape],[])
    AS_IF([test "x$MINIASCAPE" = "x"],
        [AC_MSG_ERROR([miniascape is not found in your PATH])],
        [AC_SUBST([MINIASCAPE],[$MINIASCAPE])])
])


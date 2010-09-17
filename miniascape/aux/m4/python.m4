#
# m4 macros for python
#
# Copyright (c) 2009, 2010 Satoru SATOH <satoru.satoh at gmail.com>
#
# License: MIT
#
# Changelog:
# 2009       satoru.satoh created
# 2010-09-17 satoru.satoh Deprecated AC_PROG_PYTHON and AC_CHECK_PYTHON_MODULE_PATH.
#                         Use AM_PATH_PYTHON instead. 
#

#
# AC_CHECK_PYTHON_MODULE (MODULE_NAME) - check if given python module is available.
#
AC_DEFUN([AC_CHECK_PYTHON_MODULE],[
    dnl AC_REQUIRE([AM_PATH_PYTHON])

    AS_IF([test "x$PYTHON" = "x"],[AC_MSG_ERROR([python is not installed])])

    AC_MSG_CHECKING([whether python module '$1' is available])
    AS_IF([$PYTHON -c "import $1" 2>/dev/null],
        [AC_MSG_RESULT([yes])],
        [AC_MSG_ERROR([no. You must install it.])])
])



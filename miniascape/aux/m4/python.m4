#
# m4 macros for python
#
# Copyright (c) 2009 Satoru SATOH <satoru.satoh at gmail.com>
#
# License: MIT
#

#
# AC_PROG_PYTHON - check if python is installed and available
#
AC_DEFUN([AC_PROG_PYTHON],[
    AC_PATH_PROG([PYTHON],[python],[])
    AS_IF([test "x$PYTHON" = "x"],
        [AC_MSG_ERROR([python is not found in your PATH])],
        [AC_SUBST([PYTHON],[$PYTHON])])
])

# 
# AC_CHECK_PYTHON_MODULE_PATH - check where python module (noarch) is installed.
#
AC_DEFUN([AC_CHECK_PYTHON_MODULE_PATH],[
    AC_REQUIRE([AC_PROG_PYTHON])

    python_modpath=`$PYTHON -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
    AS_IF([test "x$python_modpath" = "x"],
        [AC_MSG_ERROR([could not find python module path])],
        [AC_SUBST([PYTHON_MODULE_PATH],[$python_modpath])])
])

#
# AC_CHECK_PYTHON_MODULE (MODULE_NAME) - check if given python module is available.
#
AC_DEFUN([AC_CHECK_PYTHON_MODULE],[
    AC_REQUIRE([AC_PROG_PYTHON])

    AC_MSG_CHECKING([whether python module '$1' is available])
    AS_IF([$PYTHON -c "import $1" 2>/dev/null],
        [AC_MSG_RESULT([yes])],
        [AC_MSG_ERROR([no. You must install it.])])
])



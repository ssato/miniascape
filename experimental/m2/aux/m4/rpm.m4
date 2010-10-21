#
# m4 macros for rpm
#
# Copyright (c) 2009, 2010 Satoru SATOH <satoru.satoh at gmail.com>
#
# License: see the note in REAMDE at the top directory.
#

#
# AC_PROG_RPM - check if rpm is installed and available
# AC_PROG_RPMBUILD - check if rpmbuild is installed and available
#
AC_DEFUN([AC_PROG_RPM],[
    AC_PATH_PROG([RPM],[rpm],[])
    AS_IF([test "x$RPM" = "x"],
        [AC_MSG_ERROR([rpm is not found in your PATH])],
        [AC_SUBST([RPM],[$RPM])])
])
AC_DEFUN([AC_PROG_RPMBUILD],[
    AC_PATH_PROG([RPMBUILD],[rpmbuild],[])
    AS_IF([test "x$RPMBUILD" = "x"],
        [AC_MSG_ERROR([rpmbuild is not found in your PATH])],
        [AC_SUBST([RPMBUILD],[$RPMBUILD])])
])

#
# AC_CHECK_SOURCE_ZIP - specify zip extension of source archive file.
#
AC_DEFUN([AC_CHECK_SOURCE_ZIP],[
    AC_PATH_PROG([XZ],[xz],[])
    AS_IF([test "x$XZ" = "x"],
        [AC_PATH_PROG([BZIP],[bzip2],[])
         AS_IF([test "x$BZIP" = "x"],
            [AC_MSG_ERROR([Neither xz nor bzip2 are found in your PATH])],
            [AC_SUBST([SOURCE_ZIP],[bzip2])
             AC_SUBST([SOURCE_ZIP_EXT],[bz2])])],
        [AC_SUBST([SOURCE_ZIP],[xz])
         AC_SUBST([SOURCE_ZIP_EXT],[xz])])
])

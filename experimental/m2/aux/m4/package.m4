#
# m4 macros for packaging tools
#
# Copyright (c) 2009, 2010 Satoru SATOH <satoru.satoh at gmail.com>
#
# License: see the note in REAMDE at the top directory.
#

#
# AC_PROG_PACKAGE_BUILD_TOOL - check which packaging tool is available and to be used.
#
AC_DEFUN([AC_PROG_PACKAGE_BUILD_TOOL],[
    AC_PATH_PROG([RPMBUILD],[rpmbuild],[])
    AS_IF([test "x$RPMBUILD" = "x"],
        [AC_PATH_PROG([DPKG_BUILDPACKAGE],[dpkg-buildpackage],[])
         AS_IF([test "x$DPKG_BUILDPACKAGE" = "x"],
             [AC_MSG_ERROR([Neither rpmbuild nor dpkg-buildpackage are found in your PATH])],
             [AC_SUBST([PACKAGE_BUILD_TOOL],[$DPKG_BUILDPACKAGE])])],
        [AC_SUBST([PACKAGE_BUILD_TOOL],[$RPMBUILD])
         AC_SUBST([USE_RPMBUILD],[yes])
        ])
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

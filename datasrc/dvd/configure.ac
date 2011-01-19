AC_INIT([miniascape-datasrc-dvd],[0.1.20101221])
AM_INIT_AUTOMAKE([dist-xz foreign])

dnl http://www.flameeyes.eu/autotools-mythbuster/automake/silent.html
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])

AC_PROG_MKDIR_P
AC_PROG_SED

dnl
dnl It is originally defined in ../../core/configure.ac and must be changed
dnl if customized in miniascape package.
dnl
AC_SUBST([AUTOINST_NETWORK],[192.168.151])


dnl which to use for web service?
AS_IF([test -f /etc/fedora-release],[nginx=true],[nginx=false])
AC_ARG_ENABLE([nginx],
     [  --enable-nginx  Use nginx instead of apache httpd],
     [case "${enableval}" in
       yes) nginx=true ;;
       no)  nginx=false ;;
       *) AC_MSG_ERROR([bad value ${enableval} for --enable-nginx]) ;;
     esac],[nginx=$nginx])
AM_CONDITIONAL([USE_NGINX], [test x$nginx = xtrue])

wwwdatadir="/srv/www/contents"
AC_ARG_WITH([wwwdatadir],
  [AS_HELP_STRING([--with-wwwdatadir],[WWW data (contents) dir. default=$wwwdatadir])],
      [wwwdatadir=$withval])
AC_SUBST([WWWDATADIR],[$wwwdatadir])

isodatadir="/srv/isos"
AC_ARG_WITH([isodatadir],
  [AS_HELP_STRING([--with-isodatadir],[Dir to save ISO images. default=$isodatadir])],
      [isodatadir=$withval])
AC_SUBST([ISODATADIR],[$isodatadir])



AC_CONFIG_FILES([
Makefile
README
miniascape-datasrc-dvd.spec
autofs/Makefile
autofs/auto.iso
www/Makefile
])

AC_OUTPUT

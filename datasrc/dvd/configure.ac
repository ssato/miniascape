AC_INIT([miniascape-datasrc-dvd],[0.1.20101221])
dnl AM_INIT_AUTOMAKE([1.11 silent-rules foreign])
AM_INIT_AUTOMAKE([silent-rules foreign])

dnl http://www.flameeyes.eu/autotools-mythbuster/automake/silent.html
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])

dnl
dnl It is originally defined in ../../core/configure.ac and must be changed
dnl if customized in miniascape package.
dnl
AC_SUBST([AUTOINST_NETWORK],[192.168.151])


dnl which to use for web service?
AC_ARG_ENABLE([nginx],
     [  --enable-nginx  Use nginx instead of apache httpd],
     [case "${enableval}" in
       yes) nginx=true ;;
       no)  nginx=false ;;
       *) AC_MSG_ERROR([bad value ${enableval} for --enable-nginx]) ;;
     esac],[nginx=false])
AM_CONDITIONAL([USE_NGINX], [test x$nginx = xtrue])


AC_CONFIG_FILES([
Makefile
miniascape-datasrc-dvd.spec
autofs/Makefile
httpd/Makefile
httpd/miniascape-datasrc-dvd.conf
nginx/Makefile
nginx/miniascape-datasrc-dvd.conf
])

AC_OUTPUT

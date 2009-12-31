#
# m4 macros for kickstart installation.
#
# Copyright (c) 2009 Satoru SATOH <satoru.satoh@gmail.com>
#
# License: see the note in REAMDE[.in] file at the top directory.
#

#
# AC_DEFINE_KICKSTART (KSTREE-SERVER, KSTREE-LOCATION, KSCFG-LOCATION)
# - define kickstart related parameters.
#
AC_DEFUN([AC_DEFINE_KICKSTART],[
    kstree_server=$1
    kstree_location=$2
    kscfg_location=$3

    AC_ARG_WITH([kstree-server],
        [AS_HELP_STRING([--with-kstree-server],[Real server to provide kickstart tree. default=$kstree_server])],
        [kstree_server=$withval],[])
    AC_SUBST([KICKSTART_TREE_SERVER],[$kstree_server])

    AC_ARG_WITH([kstree-location],
        [AS_HELP_STRING([--with-kstree-location],[Kickstart tree location. default=$kstree_location])],
        [kstree_location=$withval],[])
    AC_SUBST([KICKSTART_TREE_LOCATION],[$kstree_location])

    AC_ARG_WITH([kscfg-location],
        [AS_HELP_STRING([--with-kscfg-location],[Kickstart cfgs location. default=$kscfg_location])],
        [kstree_location=$withval],[])
    AC_SUBST([KICKSTART_CFG_LOCATION],[$kscfg_location])

])


#
# AC_DEFINE_RHEL_INSTALLATION_KEY (KEY)
# - define rhel installation key required during installation since rhel5.
#
AC_DEFUN([AC_DEFINE_RHEL_INSTALLATION_KEY],[
    rhel_installation_key="$1"

    AC_ARG_WITH([rhel-installation-key],
        [AS_HELP_STRING([--with-rhel-installation-key],[RHEL Installation key])],
        [rhel_installation_key=$withval],[])
    AC_SUBST([RHEL_INSTALLATION_KEY],[$rhel_installation_key])

    AS_IF([test -n "$rhel_installation_key"],
        [kickstart_rhel_key="key $rhel_installation_key"],
        [kickstart_rhel_key="key --skip"])
    AC_SUBST([KICKSTART_RHEL_KEY],[$kickstart_rhel_key])
])

#
# AC_DEFINE_KICKSTART_PASSWORD (PASSWORD) - define password in ks.cfg
#
AC_DEFUN([AC_DEFINE_KICKSTART_PASSWORD],[
    password="$1"

    AC_ARG_WITH([password],
        [AS_HELP_STRING([--with-password],[Password for root in VMs.])],
        [password=$withval],[])
    AC_SUBST([KICKSTART_PASSWORD],[$password])
])

#
# AC_HTTPD_BACKEND ([BACKEND]) - define httpd backend.
# possible backends: httpd and nginx.
#
AC_DEFUN([AC_HTTPD_BACKEND],[
    httpd_backend=nginx

    AC_ARG_WITH([httpd-backend],
        [AS_HELP_STRING([--with-httpd-backend],[Httpd backend: httpd or nginx])],
        [httpd_backend=$withval],[])

    AM_CONDITIONAL([HTTPD_BACKEND_APACHE],[test "x$httpd_backend" = "xapache"])
    AM_CONDITIONAL([HTTPD_BACKEND_NGINX],[test "x$httpd_backend" = "xnginx"])
])

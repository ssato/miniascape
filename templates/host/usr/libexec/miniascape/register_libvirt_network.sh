#! /bin/bash
#
# Register libvirt virtual network.
#
# License: MIT
# Author: Satoru SATOH <ssato@redhat.com>
#
set -e

curdir=${0%/*}
usage="Usage: $0 [Options] NET_NAME"

# defaults:
netconfdir="${curdir}/../../share/libvirt/networks"
instdir="${curdir}/../../../etc/libvirt/qemu/networks"

function show_help () {
    cat << EOH
${usage:?}
Options:
    -d DATADIR    specify the dir where libvirt network xml are [$netconfdir]
    -i INSTDIR    specify the dir where libvirt registered network xml are
                  [$instdir]
    -h            show this help
EOH
}

function is_libvirtd_running () {
    if `systemctl --version`; then
        systemctl status libvirtd >/dev/null 2>/dev/null && echo "true" || echo "false"
    else
        service libvirtd status >/dev/null 2>/dev/null && echo "true" || echo "false"
    fi
}

function register_network() {
    local net=$1
    local netconfdir=$2
    local instdir=$3
    local netxml=${net:?}.xml
    local netxml_src=${netconfdir:?}/${netxml}
    local netxml_inst=${instdir:?}/${netxml}

    if test ! -f ${netxml_src}; then
        echo "[Error] network xml ${netxml_src} does not exist!"
        exit 1
    fi

    if `is_libvirtd_running`; then
        if `virsh net-list --all | grep -q ${net} 2>/dev/null`; then
            echo "Network $net already exists. Nothing to do..."
        else
            virsh net-define ${netxml_src} && \
            virsh net-start ${net} && virsh net-autostart ${net}
        fi
    else
        if test -f ${netxml_inst}; then
            echo "Found XML def file of $net (already registered ?). Nothing to do..."
        else
            # The following code snippet is originally copy-n-paste from
            # libvirt.spec.in in libvirt git repo which is distributed under
            # LGPLv2+ license.
            uuid=`/usr/bin/uuidgen`
            (cd $instdir/autostart && \
             sed -e "s,</name>,</name>\n  <uuid>${uuid:?}</uuid>," ${netxml_src} > ../${netxml} && \
             ln -s ../${netxml} ./)
        fi
    fi
}

# main:
if test $# -lt 1; then
    echo ${usage}
    exit 0
fi

while getopts "d:i:h" opt
do
    case $opt in
        d) netconfdir=$OPTARG ;;
        i) instdir=$OPTARG ;;
        h) show_help; exit 0 ;;
        \?) show_help; exit 1 ;;
    esac
done
shift $(($OPTIND - 1))

net=$1

register_network ${net} ${netconfdir} ${instdir}
exit $?

# vim:sw=4:ts=4:et:

#! /bin/bash
#
# A quick and *very* dirty hack to register DNS and DHCP entry of given guests
# to libvirt NAT-ed virtual network.
#
# License: MIT
# Author: Satoru SATOH <ssato@redhat.com>
#
set -e

# defaults:
network=default
macaddr=random

function show_help () {
    cat << EOH
Usage: $0 [Options] FQDN IP
Options:
  -n    specify libvirt's virtual network [$network]
  -m    specify MAC address of the guest, or special keyword 'random' to
        generate random mac address, or 'no' not to register DHCP entry for
        the guest [$macaddr]
  -h    show this help
EOH
}

function gen_macaddr () {
    local prefix=$1
    test "x${prefix}" = "x" && prefix="52:54:00"
    dd if=/dev/urandom bs=1024 count=1 2>/dev/null | md5sum | \
        sed "s/^\(..\)\(..\)\(..\).*$/${prefix}:\1:\2:\3/"
}

if test $# -lt 2; then
    show_help
    exit 0
fi

while getopts "n:m:h" opt
do
    case $opt in
        n) network=$OPTARG ;;
        m) macaddr=$OPTARG ;;
        h) show_help; exit 0 ;;
        \?) show_help; exit 1 ;;
    esac
done
shift $(($OPTIND - 1))

fqdn=$1
ip=$2

if test "$macaddr" = "random"; then
    macaddr=`gen_macaddr`
    echo "[Info] Generated mac address: $macaddr"
else
    test "$macaddr" = "no" && macaddr=""
fi

# files:
net_def=/etc/libvirt/qemu/networks/${network}.xml
dns_map=/var/lib/libvirt/dnsmasq/${network}.addnhosts
dhcp_map=/var/lib/libvirt/dnsmasq/${network}.hostsfile

function dnsmasq_reload () {
    local pidfile=/var/run/libvirt/network/${network}.pid
    test -f $pidfile && kill -HUP $(cat $pidfile)
}

function register_dns_host () {
    local network=$1
    local ip=$2
    local fqdn=$3

    # Check if the target entry exist in DNS map file of dnsmasq run by
    # libvirtd:
    if `grep -q ${fqdn} ${dns_map} 2>/dev/null`; then
        echo "The DNS entry for ${fqdn} already exist! Nothing to do..."
    else
        # FIXME: The part 'sed ...' is a quick and dirty hack.
        echo "Adding DNS entry of ${fqdn} to the network ${network}..."
        dns_entry="<host ip='${ip}'><hostname>${fqdn}</hostname></host>"
        virsh net-update --config --live ${network} add dns-host "${dns_entry}" || \
        ((grep -q "</dns>" ${net_def} 2>/dev/null && \
          sed -i.save "s,</dns>,    ${dns_entry}\n   </dns>," ${net_def} ||
          sed -i.save "s,</network>,  <dns>\n    ${dns_entry}\n  </dns>\n</network>," ${net_def}) && \
         echo "${ip}  ${fqdn}" >> ${dns_map} && dnsmasq_reload && \
         virsh net-define ${net_def})
    fi
}

function register_dhcp_host () {
    local network=$1
    local macaddr=$2
    local ip=$3
    local fqdn=$4

    if `grep -q ${macaddr} ${dhcp_map} 2>/dev/null`; then
        echo "The DHCP entry for ${macaddr} already exist! Nothing to do..."
    else
        echo "Adding DHCP entry of ${fqdn} to the network ${network}..."
        dhcp_entry="<host mac='${macaddr}' name='${fqdn}' ip='${ip}' />"
        virsh net-update --config --live ${network} add ip-dhcp-host "${dhcp_entry}" || \
        (sed -i.save "s,</dhcp>,  ${dhcp_entry}\n    </dhcp>," ${net_def} && \
         echo "${macaddr},${ip},${fqdn}" >> ${dhcp_map} && dnsmasq_reload && \
         virsh net-define ${net_def})
    fi
}

if test -f ${net_def}; then
    if test "x$macaddr" = "x"; then
        echo "[Info] MAC address was not given. Do not add DHCP entry for this guest."
    else
        register_dhcp_host ${network} ${macaddr} ${ip} ${fqdn}; rc=$?
        if test $rc != 0; then
            echo "Failed to register DHCP host entry: mac=${macaddr}, ip=${ip}, fqdn=${fqdn}"
            exit $rc
        fi
    fi
    register_dns_host ${network} ${ip} ${fqdn}; rc=$?
    if test $rc != 0; then
        echo "Failed to register DNS host entry: ip=${ip}, fqdn=${fqdn}"
        exit $rc
    fi
else
    echo "The network ${network} does not exist! Register it first"
    exit 1
fi

exit $rc

# vim:sw=4:ts=4:et:

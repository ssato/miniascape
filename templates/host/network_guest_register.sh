#! /bin/bash
#
# A tiny script to register DNS and DHCP entry of given guests to libvirt
# NAT-ed virtual network.
#
# License: MIT
# Author: Satoru SATOH <ssato@redhat.com>
#
set -e
network=$1  # Virtual network name, e.g. 'default'
ip=$2       # ip address
fqdn=$4     # fqdn
mac=$4      # mac address

if test $# -lt 3; then
    echo "Usage: $0 NETWORK_NAME IP FQDN [MAC_ADDR]"
    exit 0
fi

function register_dns_host () {
    network=$1
    ip=$2
    fqdn=$3

    # Check if the target entry exist in DNS map file of dnsmasq run by
    # libvirtd:
    if `grep -q ${ip:?} /var/lib/libvirt/dnsmasq/${network:?}.addnhosts 2>/dev/null`; then
        echo "The DNS entry for ${fqdn:?} already exist! Nothing to do..."
    else
        echo "Adding DNS entry of ${fqdn:?} to the network ${network}..."
        virsh net-update --config --live ${network} add dns-host "<host ip='${ip}'><hostname>${fqdn}</hostname></host>"
    fi
}

function register_dhcp_host () {
    network=$1
    mac=$2
    ip=$3
    fqdn=$4

    # DNS
    if `grep -q ${mac:?} /var/lib/libvirt/dnsmasq/${network:?}.hostsfile 2>/dev/null`; then
        echo "The DHCP entry for ${mac:?} already exist! Nothing to do..."
    else
        echo "Adding DHCP entry of ${fqdn:?} to the network ${network}..."
        virsh net-update --config --live ${network} add ip-dhcp-host "<host mac='${mac:?}' name='${fqdn}' ip='${ip}' />"
    fi
}

if test -f /etc/libvirt/qemu/networks/${network:?}.xml; then
    register_dns_host ${network} ${ip} ${fqdn}; rc=$?
    if test $rc != 0; then
        echo "Failed to register DNS host entry: ip=${ip}, fqdn=${fqdn}"
        exit $rc
    fi

    if test "x$mac" != "x"; then
        register_dhcp_host ${network} ${mac} ${ip} ${fqdn}; rc=$?
        if test $rc != 0; then
            echo "Failed to register DHCP host entry: mac=${mac}, ip=${ip}, fqdn=${fqdn}"
            exit $rc
        fi
    fi
else
    echo "The network ${network} does not exist! Register it first"
    exit 1
fi

exit $rc

# vim:sw=4:ts=4:et:

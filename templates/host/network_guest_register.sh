#! /bin/bash
set -e
network=$1  # Virtual network name, e.g. 'default'
mac=$2      # mac address
ip=$3       # ip address
fqdn=$4     # fqdn

function register_dns_host () {
    network=$1
    ip=$2
    fqdn=$3

    # DNS
    if `grep -q ${ip:?} /var/lib/libvirt/dnsmasq/${network:?}.addnhosts 2>/dev/null`; then
        echo "The DNS entry for ${fqdn:?} already exist! Nothing to do..."
    else
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
        virsh net-update --config --live ${network} add ip-dhcp-host "<host mac='${mac:?}' name='${fqdn}' ip='${ip}' />"
    fi
}

if test -f /etc/libvirt/qemu/networks/${network:?}.xml; then
    register_dns_host ${network} ${ip} ${fqdn}; rc=$?
    if test $rc != 0; then
        echo "Failed to register DNS host entry: ip=${ip}, fqdn=${fqdn}"
        exit $rc
    fi

    register_dhcp_host ${network} ${mac} ${ip} ${fqdn}; rc=$?
    if test $rc != 0; then
        echo "Failed to register DHCP host entry: mac=${mac}, ip=${ip}, fqdn=${fqdn}"
        exit $rc
    fi
else
    echo "The network ${network} does not exist! Register it first"
    exit 1
fi

exit $rc

# vim:sw=4:ts=4:et:

#! /bin/bash
#
# A tiny script to register DNS and DHCP entry of given guests to libvirt
# NAT-ed virtual network.
#
# License: MIT
# Author: Satoru SATOH <ssato@redhat.com>
#
set -e
ip=$1       # ip address
fqdn=$2     # fqdn
network=$3  # virtual network name, e.g. 'default'
mac=$4      # mac address

if test $# -lt 2; then
    echo "Usage: $0 IP FQDN [NETWORK_NAME] [MAC_ADDR]"
    exit 0
fi

# Default network to apply changes:
test "x$network" = "x" && network="default"

# files:
net_def=/etc/libvirt/qemu/networks/${network}.xml
dns_map=/var/lib/libvirt/dnsmasq/${network}.addnhosts
dhcp_map=/var/lib/libvirt/dnsmasq/${network}.hostsfile


function dnsmasq_reload () {
    local pidfile=/var/run/libvirt/network/${network}.pid
    test -f $pidfile && kill -HUP $(cat $pidfile)
}

function register_dns_host () {
    network=$1
    ip=$2
    fqdn=$3

    # Check if the target entry exist in DNS map file of dnsmasq run by
    # libvirtd:
    if `grep -q ${fqdn} ${dns_map} 2>/dev/null`; then
        echo "The DNS entry for ${fqdn} already exist! Nothing to do..."
    else
        echo "Adding DNS entry of ${fqdn} to the network ${network}..."
        dns_entry="<host ip='${ip}'><hostname>${fqdn}</hostname></host>"
        virsh net-update --config --live ${network} add dns-host "${dns_entry}" || \
        (sed -e "s,</dns>,    ${dns_entry}\n   </dns>," \
            ${net_def} > ${network}.save && mv ${net_def}.save ${net_def} && \
            echo "${ip}  ${fqdn}" >> ${dns_map} && dnsmasq_reload
    fi
}

function register_dhcp_host () {
    network=$1
    mac=$2
    ip=$3
    fqdn=$4

    if `grep -q ${mac} ${dhcp_map} 2>/dev/null`; then
        echo "The DHCP entry for ${mac} already exist! Nothing to do..."
    else
        echo "Adding DHCP entry of ${fqdn} to the network ${network}..."
        dhcp_entry="<host mac='${mac}' name='${fqdn}' ip='${ip}' />"
        virsh net-update --config --live ${network} add ip-dhcp-host "${dhcp_entry}" || \
        (sed -e "s,</dhcp>,    ${dhcp_entry}\n    </dhcp>," \
            ${net_def} > ${net_def}.save && mv ${net_def}.save ${net_def}.xml && \
            echo "${mac},${ip},${fqdn}" >> ${dhcp_map} && dnsmasq_reload \
    fi
}

if test -f ${net_def}; then
    register_dns_host ${network} ${ip} ${fqdn}; rc=$?
    if test $rc != 0; then
        echo "Failed to register DNS host entry: ip=${ip}, fqdn=${fqdn}"
        exit $rc
    fi

    if test "x$mac" = "x"; then
        echo "[Info] MAC address was not given. Do not add DHCP entry for this guest."
    else
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

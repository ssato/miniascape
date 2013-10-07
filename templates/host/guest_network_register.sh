#! /bin/bash
#
# A quick and *very* dirty hack to register DNS and DHCP entry of given guests
# to libvirt NAT-ed virtual network.
#
# License: MIT
# Author: Satoru SATOH <ssato@redhat.com>
#
# NOTEs:
# * Libvirt < 0.10.2 does not support partial dynamic network def updates
# * It seems that some versions of libvirt will fail to add DNS entry even if
#   its is newer than 0.10.2, e.g. libvirt in RHEL 6.4
#
# TODOs:
# * Dynamic IP address generation w/ ipcalc, etc.
# * Tweak DHCP range to exclude statically assigned DHCP addresses
#
set -e

# defaults:
network=default
macaddr=random
check_if_dns=no  # or 'yes'

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
    local prefix=${1:-52:54:00}  # @see virt-install(1)
    dd if=/dev/urandom bs=1024 count=1 2>/dev/null | md5sum | \
        sed "s/^\(..\)\(..\)\(..\).*$/${prefix}:\1:\2:\3/"
}

function netdef_path () {
    local network=$1
    echo "/etc/libvirt/qemu/networks/${network:?}.xml"
}

# FIXME: This is a dirty hack.
function reload_dnsmasq () {
    local network=$1
    local pidfile=/var/run/libvirt/network/${network:?}.pid
    if test -f ${pidfile}; then
        pid=$(cat ${pidfile})
        echo -n "[Info] Reloading dnsmasq: ${pid} ..." && kill -HUP ${pid}; rc=$?
        if test $rc -eq 0; then
            echo -ne "OK\n"
        else
            echo -ne "Failure!\n"
            exit $rc
        fi
    else
        echo "[Info] dnsmasq does not look running. Nothing to do..." 
    fi
}

function register_dns_host () {
    local network=$1
    local ip=$2
    local fqdn=$3
    local dns_map=/var/lib/libvirt/dnsmasq/${network:?}.addnhosts
    local dns_entry="<host ip='${ip:?}'><hostname>${fqdn:?}</hostname></host>"
    local net_def=$(netdef_path ${network})

    # Check if the target entry exist in DNS map file of dnsmasq run by
    # libvirtd:
    if `grep -q ${fqdn} ${dns_map} 2>/dev/null`; then
        echo "[Info] The DNS entry for ${fqdn} already exist! Nothing to do..."
    else
        # FIXME: The part 'sed ...' is a quick and dirty hack.
        echo "[Info] Adding DNS entry of ${fqdn} to the network ${network}..."
        virsh net-update --config --live ${network} add dns-host "${dns_entry}" || \
        ((grep -q "</dns>" ${net_def} 2>/dev/null && \
          sed -i.save "s,</dns>,    ${dns_entry}\n   </dns>," ${net_def} ||
          sed -i.save "s,</network>,  <dns>\n    ${dns_entry}\n  </dns>\n</network>," ${net_def}) && \
         echo "${ip}  ${fqdn}" >> ${dns_map} && reload_dnsmasq ${network} && \
         virsh net-define ${net_def})
    fi
}

function register_dhcp_host () {
    local network=$1
    local macaddr=$2
    local ip=$3
    local fqdn=$4
    local dhcp_map=/var/lib/libvirt/dnsmasq/${network:?}.hostsfile
    local dhcp_entry="<host mac='${macaddr:?}' name='${fqdn:?}' ip='${ip:?}'/>"
    local net_def=$(netdef_path ${network})
    local domain=${fqdn#*.}

    if $(grep -q ${macaddr} ${dhcp_map} 2>/dev/null); then
        echo "[Info] The DHCP entry for ${macaddr} already exist! Nothing to do..."
    else
        echo "[Info] Adding DHCP entry of ${fqdn} to the network ${network}..."
        if ! $(virsh net-update --config --live ${network} add ip-dhcp-host "${dhcp_entry}"); then
            if $(grep -q "<domain name=" ${net_def} 2>/dev/null); then
                sed -i.save -e "s,</dhcp>,  ${dhcp_entry}\n    </dhcp>," ${net_def}
            else
                echo "[Info] Domain entry ${domain} will also be added."
                sed -i.save -e "s,</dhcp>,  ${dhcp_entry}\n    </dhcp>," \
                    -e "s,</network>,  <domain name='${domain}'/>\n</network>," ${net_def}
            fi
            echo "${macaddr},${ip},${fqdn}" >> ${dhcp_map} && reload_dnsmasq ${network} && \
            virsh net-define ${net_def}
        fi
    fi
}

function print_ssh_config () {
    local ip=$1
    local fqdn=$2
    local hostname=$(echo ${fqdn:?} | cut -f 1 -d '.')
    test "x$ip" != "x"  # assert

    cat << EOC

# Sample configuration to access for this guest in ~/.ssh/config:
Host ${hostname}
  Hostname ${ip}
  User root
EOC
}

function check_dns_host () {
    local network=$1
    local ip=$2
    local fqdn=$3
    local net_def=$(netdef_path ${network:?})

    # The gateway (libvirt host) should also provide DNS service:
    local gateway=$(sed -nr "s/.*<ip address=.([^\"\']+). .*/\1/p" ${net_def})

    echo -n "[Info] Try resolving DNS entry for ${fqdn:?} ... "
    if $(host ${fqdn} ${gateway:?} > /dev/null); then
        echo "OK"
    else
        echo "Failure!"
        exit 1
    fi
}

# main:
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

if test "x$macaddr" = "xrandom"; then
    macaddr=$(gen_macaddr)
    echo "[Info] Generated mac address: $macaddr"
else
    test "x$macaddr" = "xno" && macaddr=""
fi

net_def=$(netdef_path ${network})
if test -f ${net_def}; then
    if test "x$macaddr" = "x"; then
        echo "[Info] MAC address was not given. Do not add DHCP entry for this guest."
    else
        register_dhcp_host ${network} ${macaddr} ${ip} ${fqdn}; rc=$?
        if test $rc != 0; then
            echo "[Error] Failed to add DHCP entry: mac=${macaddr}, ip=${ip}, fqdn=${fqdn}"
            exit $rc
        fi
    fi
    register_dns_host ${network} ${ip} ${fqdn}; rc=$?
    test "x${check_if_dns}" = "xyes" && check_dns_host ${network} ${ip} ${fqdn} || :
    if test $rc = 0; then
        print_ssh_config ${ip} ${fqdn}
    else
        echo "[Error] Failed to add DNS host entry: ip=${ip}, fqdn=${fqdn}"
        exit $rc
    fi
else
    echo "[Error] The network ${network} does not exist! Register it first."
    exit 1
fi

exit $rc

# vim:sw=4:ts=4:et:

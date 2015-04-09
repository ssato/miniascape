#! /bin/bash
#set -e

selfdir=${0%/*}
source ${selfdir:?}/pre.dynamic_network.rhel-7.functions

BOOT_PARAMS_0='...
ip="192.168.122.101::192.168.122.1:255.255.255.0:rhel-7-srv-1.example.com:bond0:none"
ip="192.168.100.11::192.168.100.254:255.255.0.0::bond1:none"
bond="bond0:em1,em2:mode=active-backup,downdelay=5000"
bond="bond1:em3,em4"
bootdev="bond0"
'

test_find_bootdev__match () {
    test x$(find_bootdev 'bootdev="bond0"') = 'xbond0'
}

test_find_bootdev__not_match () {
    test x$(find_bootdev 'bond="bond1:em3,em4"') = x
    test x$(find_bootdev 'ip="192.168.100.11::192.168.100.254:255.255.0.0::bond1:none"') = x
}

test_parse_bond_spec__match () {
    test "x$(parse_bond_spec 'bond0:eth0,eth3')" = 'xbond=bond0; slaves=eth0,eth3; bond_opts=""' 
    test "x$(parse_bond_spec 'bond1:em1,em2:mode=active-backup')" = \
         'xbond=bond1; slaves=em1,em2; bond_opts="mode=active-backup"'
}

test_parse_bond_spec__not_match () {
    test x$(parse_bond_spec "em1:") = x
}

test_parse_ip_spec__auto_config_all_bootproto__match () {
    test x$(parse_ip_spec__auto_config_all_bootproto "dhcp") = "xdhcp"
    test x$(parse_ip_spec__auto_config_all_bootproto "ibft") = "xibft"
}

test_parse_ip_spec__auto_config_all_bootproto__not_match () {
    test x$(parse_ip_spec__auto_config_all_bootproto "em1:dhcp") = x
    test x$(parse_ip_spec__auto_config_all_bootproto "192.168.100.11::192.168.100.254:255.255.0.0::bond1:none") = x
}

IP_LINK_OUT_0='
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default \    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: enp0s25: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000\    link/ether xx:xx:xx:xx:xx:xx brd ff:ff:ff:ff:ff:ff
3: wlp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DORMANT group default qlen 1000\    link/ether xx:xx:xx:xx:xx:xx brd ff:ff:ff:ff:ff:ff
4: virbr5: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default \    link/ether 52:54:00:dd:f6:ec brd ff:ff:ff:ff:ff:ff
6: virbr2: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default \    link/ether 52:54:00:71:98:f7 brd ff:ff:ff:ff:ff:ff
8: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default \    link/ether 52:54:00:a9:60:9c brd ff:ff:ff:ff:ff:ff
'
IFACE_LIST_0='enp0s25 wlp3s0'

# FIXME:
TODO_test_list_linkup_interfaces__match () {
    test "x$(list_linkup_interfaces \"${IP_LINK_OUT_0}\") | tr '\n' ' '" = "x${IFACE_LIST_0}"
}

test_parse_ip_spec__auto_config__match () {
    test "x$(parse_ip_spec__auto_config 'em0:dhcp6')" = 'xiface=em0; method=dhcp6; bootproto=dhcp'
}

test_parse_ip_spec__auto_config__not_match () {
    test "x$(parse_ip_spec__auto_config 'dhcp6')" = x
    test "x$(parse_ip_spec__auto_config '192.168.100.11::192.168.100.254:255.255.0.0::bond1:none')" = x
}

test_parse_ip_spec__static_config__match () {
    test "x$(parse_ip_spec__static_config '192.168.122.101::192.168.122.1:255.255.255.0:rhel-7-srv-1.example.com:bond0:none')" = \
         'xip=192.168.122.101; gateway=192.168.122.1; netmask=255.255.255.0; hostname=rhel-7-srv-1.example.com; iface=bond0'
    test "x$(parse_ip_spec__static_config '192.168.100.11::192.168.100.254:255.255.0.0::bond1:none')" = \
         'xip=192.168.100.11; gateway=192.168.100.254; netmask=255.255.0.0; hostname=; iface=bond1'
}

test_parse_ip_spec__static_config__not_match () {
    test "x$(parse_ip_spec__static_config 'dhcp6')" = x
    test "x$(parse_ip_spec__static_config 'em0:dhcp')" = x
}

for test_func in $(sed -nr 's/^(test_[^\( ]+) .*/\1/p' $0); do
    echo "${test_func}: $(${test_func} && echo OK || echo NG)"
done

# vim:sw=4:ts=4:et:

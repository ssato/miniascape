#! /bin/bash

oneTimeSetUp () {
    . ${0%/*}/../../../../templates/autoinstall.d/snippets/pre.dynamic_network.rhel-7.functions
}

test_find_boottev () {
    assertEquals $(find_bootdev bootdev=eth1) eth1
}

test_parse_bond_spec_00_wo_opts () {
    assertEquals $(parse_bond_spec "bond1:em3,em4") 'bond=bond1;slaves=em3,em4;bond_opts='
}

test_parse_bond_spec_10_w_opts () {
    assertEquals \
        $(parse_bond_spec "bond0:em1,em2:mode=active-backup,downdelay=5000") \
        'bond=bond0;slaves=em1,em2;bond_opts=mode=active-backup,downdelay=5000'
}

test_parse_ip_spec__auto_config_all_bootproto () {
    assertEquals $(parse_ip_spec__auto_config_all_bootproto ibft) ibft
    assertEquals $(parse_ip_spec__auto_config_all_bootproto dhcp) dhcp
    assertEquals $(parse_ip_spec__auto_config_all_bootproto dhcp6) dhcp
}

test_list_linkup_interfaces() {
    input='\
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1\    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: enp0s25: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000\    link/ether xx:xx:xx:xx:xx:xx brd ff:ff:ff:ff:ff:ff
4: virbr1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default qlen 1000\    link/ether xx:xx:xx:xx:xx:xx brd ff:ff:ff:ff:ff:ff
6: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default \    link/ether xx:xx:xx:xx:xx:xx brd ff:ff:ff:ff:ff:ff
7: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default qlen 1000\    link/ether xx:xx:xx:xx:xx:xx brd ff:ff:ff:ff:ff:ff
'
    assertEquals $(list_linkup_interfaces "${input}") "enp0s25"
}

test_parse_ip_spec__auto_config () {
    assertEquals $(parse_ip_spec__auto_config "em2:dhcp") "iface=em2;method=dhcp;bootproto=dhcp"
}

test_parse_ip_spec__static_config () {
    assertEquals $(parse_ip_spec__static_config \
        '192.168.122.100::192.168.122.1:255.255.255.0:foo.example.com:em1:none') \
    'ip=192.168.122.100;gateway=192.168.122.1;netmask=255.255.255.0;hostname=foo.example.com;iface=em1'
}

. /usr/share/shunit2/shunit2
# vim:sw=4:ts=4:et:

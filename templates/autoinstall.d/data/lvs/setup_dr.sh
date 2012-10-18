# Requirements: sysctl
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
# References:
# * http://red.ht/WlYyYo
# * http://www.austintek.com/LVS/LVS-HOWTO/HOWTO/LVS-HOWTO.LVS-DR.html
#
# Notes:
#
# """There's no forwarding in the conventional sense for LVS-DR (ip_vs does the
# forwarding on the director of the LVS packets). You can have ip_forward set
# to ON if you need it for something else, but LVS_DR doesn't need in ON. If
# you don't have a good reason to have it ON, then for security turn it OFF.
# For more explanation see design of ipvs for netfilter."""
#
# [LVS Howto, 7.2. How LVS-DR works] (above link)
#
sed -i.save /etc/sysctl.conf -r "s/^(net.ipv4.ip_forward =) 0/\1 1\nnet.ipv4.conf.all.promote_secondaries = 1/g"
/sbin/sysctl -p

/sbin/service iptables save
cp -f /etc/sysconfig/iptables /etc/sysconfig/iptables.save
# Firewall marks for FTP
# Rules for FTP passive connections in LVS (http://red.ht/OBrlF3):
/sbin/service iptables -t mangle -A PREROUTING -p tcp -d {{ lvs.public.ip.addr }}/{{ lvs.public.ip.maskbit }} --dport 20 -j MARK --set-mark 21
/sbin/service iptables -t mangle -A PREROUTING -p tcp -d {{ lvs.public.ip.addr }}/{{ lvs.public.ip.maskbit }} --dport 21 -j MARK --set-mark 21
/sbin/service iptables -t mangle -A PREROUTING -p tcp -d {{ lvs.public.ip.addr }}/{{ lvs.public.ip.maskbit }} --dport 10000:20000 -j MARK --set-mark 21
/sbin/service iptables save

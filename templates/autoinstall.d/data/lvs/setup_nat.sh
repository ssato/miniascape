# Requirements: sysctl, iptables
# Author: Satoru SATOH <ssato@redhat.com>
# License: MIT
#
cp /etc/sysctl.conf /etc/sysctl.conf.save
cat << EOF >> /etc/sysctl.conf
net.ipv4.ip_forward = 1
net.ipv4.conf.all.promote_secondaries = 1
EOF
/sbin/sysctl -p

/sbin/iptables save
cp /etc/sysconfig/iptables /etc/sysconfig/iptables.save
# Firewall marks for HTTP, HTTPS
/sbin/iptables -t mangle -A PREROUTING -p tcp -d {{ lvs.private.ip.addr }}/{{ lvs.private.ip.maskbit }} -m multiport --dports 80,443 -j MARK --set-mark 80
# Rules for FTP active connections in LVS:
# Allows this LVS router to accept outgoing FTP connections from real servers
# that IPVS does not know about (http://red.ht/R6HsJn):
/sbin/iptables -t nat -A POSTROUTING -p tcp -s {{ lvs.private.ip.network }}/{{ lvs.private.ip.maskbit }} --sport 20 -j MASQUERADE
# Rules for FTP passive connections in LVS (http://red.ht/OBrlF3):
/sbin/iptables -t mangle -A PREROUTING -p tcp -d {{ lvs.private.ip.addr }}/{{ lvs.private.ip.maskbit }} --dport 21 -j MARK --set-mark 21
/sbin/iptables -t mangle -A PREROUTING -p tcp -d {{ lvs.private.ip.addr }}/{{ lvs.private.ip.maskbit }} --dport 10000:20000 -j MARK --set-mark 21 
/sbin/iptables save

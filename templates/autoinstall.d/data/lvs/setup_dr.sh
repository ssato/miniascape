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
test -f /etc/sysconfig/iptables.save || cp /etc/sysconfig/iptables /etc/sysconfig/iptables.save
# Firewall marks for FTP
# Rules for FTP passive connections in LVS (http://red.ht/OBrlF3):
iptables -t mangle -A PREROUTING -p tcp -d {{ lvs.public.ip.addr }}/{{ lvs.public.ip.maskbit }} --dport 20 -j MARK --set-mark 21
iptables -t mangle -A PREROUTING -p tcp -d {{ lvs.public.ip.addr }}/{{ lvs.public.ip.maskbit }} --dport 21 -j MARK --set-mark 21
iptables -t mangle -A PREROUTING -p tcp -d {{ lvs.public.ip.addr }}/{{ lvs.public.ip.maskbit }} --dport 10000:20000 -j MARK --set-mark 21
/sbin/service iptables save
/sbin/service iptables restart

test -f /etc/sysconfig/ha/lvs.cf.save || cp /etc/sysconfig/ha/lvs.cf /etc/sysconfig/ha/lvs.cf.save
cat << EOF > /etc/sysconfig/ha/lvs.cf
serial_no = 1
primary = {{ lvs.routers.primary }}
service = lvs
backup = {{ lvs.routers.backup }}
heartbeat = 1
heartbeat_port = 539
keepalive = 6
deadtime = 18
network = direct
debug_level = NONE
virtual web {
     active = 1
     address = {{ lvs.public.ip.addr }} eth0:1
     vip_nmask = 255.255.255.0
     port = 80
     send = "GET / HTTP/1.0\r\n\r\n"
     expect = "HTTP"
     use_regex = 0
     load_monitor = none
     scheduler = rr
     protocol = tcp
     timeout = 6
     reentry = 15
     quiesce_server = 0
{% for rs in lvs.rs %}     server {{ rs.hostname }} {
         address = {{ rs.ip }}
         active = 1
         weight = 1
     }
{% endfor %}
}
virtual ftp {
     active = 1
     address = {{ lvs.public.ip.addr }} eth0:1
     vip_nmask = 255.255.255.0
     fwmark = 21
     port = 21
     persistent = 1
     send = "quit"
     expect = "220"
     load_monitor = none
     scheduler = rr
     protocol = tcp
     timeout = 6
     reentry = 15
     quiesce_server = 0
{% for rs in lvs.rs %}     server {{ rs.hostname }} {
         address = {{ rs.ip }}
         active = 1
         weight = 1
     }
{% endfor %}
}
EOF

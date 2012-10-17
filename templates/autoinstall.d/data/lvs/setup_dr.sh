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
#
cp /etc/sysctl.conf /etc/sysctl.conf.save
cat << EOF >> /etc/sysctl.conf
net.ipv4.conf.all.promote_secondaries = 1
EOF
/sbin/sysctl -p

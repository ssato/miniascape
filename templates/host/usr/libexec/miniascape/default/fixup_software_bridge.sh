#! /bin/sh
# Avoid a bug in linux kernel's software bridge bug in multicast_snooping:
brdev=${1:-{{ bridge|default('virbr0') }}}
echo 0 > /sys/class/net/${brdev}/bridge/multicast_snooping

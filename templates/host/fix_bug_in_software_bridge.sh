#! /bin/sh
# Avoid a bug in linux kernel's software bridge bug in multicast_snooping:
echo 0 > /sys/class/net/{{ bridge|default('virbr0') }}/bridge/multicast_snooping

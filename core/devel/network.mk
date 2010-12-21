#
# Makefile for vg-manage
#

## Networks:
miniascape_NET_1_MODEL	?= $(miniascape_NET_MODEL_DEFAULT)

ifneq ($(miniascape_NETWORK_2),)
miniascape_NET_2_MODEL	?= $(miniascape_NET_MODEL_DEFAULT)
network_opts += --network=$(miniascape_NETWORK_2),model=$(miniascape_NET_2_MODEL),mac=$(miniascape_MAC_2)
endif
ifneq ($(miniascape_NETWORK_3),)
miniascape_NET_3_MODEL	?= $(miniascape_NET_MODEL_DEFAULT)
network_opts += --network=$(miniascape_NETWORK_3),model=$(miniascape_NET_3_MODEL),mac=$(miniascape_MAC_3)
endif
ifneq ($(miniascape_NETWORK_4),)
miniascape_NET_4_MODEL	?= $(miniascape_NET_MODEL_DEFAULT)
network_opts += --network=$(miniascape_NETWORK_4),model=$(miniascape_NET_4_MODEL),mac=$(miniascape_MAC_4)
endif


# targets:
check-network-vars:
	test -z "$(miniascape_NETWORK_2)" || test -n "$(miniascape_NETWORK_2)" -a -n "$(miniascape_MAC_2)"
	test -z "$(miniascape_NETWORK_3)" || test -n "$(miniascape_NETWORK_3)" -a -n "$(miniascape_MAC_3)"
	test -z "$(miniascape_NETWORK_4)" || test -n "$(miniascape_NETWORK_4)" -a -n "$(miniascape_MAC_4)"


.PHONY: check-network-vars
# vim:set ft=make ai si sm:

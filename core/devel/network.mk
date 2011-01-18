#
# lib. makefiles - network stuff
#

ifeq ($(miniascape_NET_NETWORK_1),)
$(error You must specify miniascape_NET_NETWORK_1, that is, single network interface is needed for a VM at least.)
endif

miniascape_NET_1_MODEL	?= $(miniascape_NET_MODEL)
miniascape_MAC_1	?= $(miniascape_NET_MAC)
network_opts	= --network=$(miniascape_NET_NETWORK_1),model=$(miniascape_NET_1_MODEL),mac=$(miniascape_MAC_1)


ifneq ($(miniascape_NET_NETWORK_2),)
miniascape_NET_2_MODEL	?= $(miniascape_NET_MODEL)
miniascape_MAC_2	?= $(miniascape_NET_MAC)
network_opts += --network=$(miniascape_NET_NETWORK_2),model=$(miniascape_NET_2_MODEL),mac=$(miniascape_MAC_2)
endif

ifneq ($(miniascape_NET_NETWORK_3),)
miniascape_NET_3_MODEL	?= $(miniascape_NET_MODEL)
miniascape_MAC_3	?= $(miniascape_NET_MAC)
network_opts += --network=$(miniascape_NET_NETWORK_3),model=$(miniascape_NET_3_MODEL),mac=$(miniascape_MAC_3)
endif

ifneq ($(miniascape_NET_NETWORK_4),)
miniascape_NET_4_MODEL	?= $(miniascape_NET_MODEL)
miniascape_MAC_4	?= $(miniascape_NET_MAC)
network_opts += --network=$(miniascape_NET_NETWORK_4),model=$(miniascape_NET_4_MODEL),mac=$(miniascape_MAC_4)
endif

# vim:set ft=make ai si sm:

#
# lib. makefiles - network stuff
#

ifeq ($(miniascape_NET_NETWORK_1),)
$(error You must specify miniascape_NET_NETWORK_1, that is, single network interface is needed for a VM at least.)
endif

miniascape_NET_1_MODEL	?= $(miniascape_NET_MODEL)
mac_1_opt	= $(shell test "x$(miniascape_MAC_1)" = "xRANDOM" -o "x$(miniascape_MAC_1)" = "x" && echo "" || echo ",mac=$(miniascape_MAC_1)")
network_opts	= --network=$(miniascape_NET_NETWORK_1),model=$(miniascape_NET_1_MODEL)$(mac_1_opt)

ifneq ($(miniascape_NET_NETWORK_2),)
miniascape_NET_2_MODEL	?= $(miniascape_NET_MODEL)
mac_2_opt	= $(shell test "x$(miniascape_MAC_2)" = "xRANDOM" -o "x$(miniascape_MAC_2)" = "x" && echo "" || echo ",mac=$(miniascape_MAC_2)")
network_opts += --network=$(miniascape_NET_NETWORK_2),model=$(miniascape_NET_2_MODEL)$(mac_2_opt)
endif

ifneq ($(miniascape_NET_NETWORK_3),)
miniascape_NET_3_MODEL	?= $(miniascape_NET_MODEL)
miniascape_MAC_3	?= $(miniascape_NET_MAC)
mac_3_opt	= $(shell test "x$(miniascape_MAC_3)" = "xRANDOM" -o "x$(miniascape_MAC_3)" = "x" && echo "" || echo ",mac=$(miniascape_MAC_3)")
network_opts += --network=$(miniascape_NET_NETWORK_3),model=$(miniascape_NET_3_MODEL)$(mac_3_opt)
endif

ifneq ($(miniascape_NET_NETWORK_4),)
miniascape_NET_4_MODEL	?= $(miniascape_NET_MODEL)
miniascape_MAC_4	?= $(miniascape_NET_MAC)
mac_4_opt	= $(shell test "x$(miniascape_MAC_4)" = "xRANDOM" -o "x$(miniascape_MAC_4)" = "x" && echo "" || echo ",mac=$(miniascape_MAC_4)")
network_opts += --network=$(miniascape_NET_NETWORK_4),model=$(miniascape_NET_4_MODEL)$(mac_4_opt)
endif

# vim:set ft=make ai si sm:

DISK_DIR	= $(miniascape_DISK_TOPDIR)/$(miniascape_NAME)

miniascape_DISK_1_SIZE     ?= $(miniascape_DISK_SIZE_DEFAULT)
miniascape_DISK_1_BUS      ?= $(miniascape_DISK_BUS_DEFAULT)
miniascape_DISK_1_PERMS	?= $(miniascape_DISK_PERMS)
miniascape_DISK_1_CACHE_MODE ?= $(miniascape_DISK_CACHE_MODE)
miniascape_DISK_1_FMT	?= $(miniascape_DISK_FMT_DEFAULT)
miniascape_DISK_1_QEMU_IMG_OPTS	?= $(miniascape_DISK_QEMU_IMG_OPTS_DEFAULT)
miniascape_DISK_2_SIZE	?= $(miniascape_DISK_SIZE_DEFAULT)
miniascape_DISK_2_BUS	?= $(miniascape_DISK_BUS_DEFAULT)
miniascape_DISK_2_PERMS	?= $(miniascape_DISK_PERMS)
miniascape_DISK_2_CACHE_MODE ?= $(miniascape_DISK_CACHE_MODE)
miniascape_DISK_2_FMT	?= $(miniascape_DISK_FMT_DEFAULT)
miniascape_DISK_2_QEMU_IMG_OPTS	?= $(miniascape_DISK_QEMU_IMG_OPTS_DEFAULT)
miniascape_DISK_3_SIZE	?= $(miniascape_DISK_SIZE_DEFAULT)
miniascape_DISK_3_BUS	?= $(miniascape_DISK_BUS_DEFAULT)
miniascape_DISK_3_PERMS	?= $(miniascape_DISK_PERMS)
miniascape_DISK_3_CACHE_MODE ?= $(miniascape_DISK_CACHE_MODE)
miniascape_DISK_3_FMT	?= $(miniascape_DISK_FMT_DEFAULT)
miniascape_DISK_3_QEMU_IMG_OPTS	?= $(miniascape_DISK_QEMU_IMG_OPTS_DEFAULT)
miniascape_DISK_4_SIZE	?= $(miniascape_DISK_SIZE_DEFAULT)
miniascape_DISK_4_BUS	?= $(miniascape_DISK_BUS_DEFAULT)
miniascape_DISK_4_PERMS	?= $(miniascape_DISK_PERMS)
miniascape_DISK_4_CACHE_MODE ?= $(miniascape_DISK_CACHE_MODE)
miniascape_DISK_4_FMT	?= $(miniascape_DISK_FMT_DEFAULT)
miniascape_DISK_4_QEMU_IMG_OPTS	?= $(miniascape_DISK_QEMU_IMG_OPTS_DEFAULT)
miniascape_DISK_5_SIZE	?= $(miniascape_DISK_SIZE_DEFAULT)
miniascape_DISK_5_BUS	?= $(miniascape_DISK_BUS_DEFAULT)
miniascape_DISK_5_PERMS	?= $(miniascape_DISK_PERMS)
miniascape_DISK_5_CACHE_MODE ?= $(miniascape_DISK_CACHE_MODE)
miniascape_DISK_5_FMT	?= $(miniascape_DISK_FMT_DEFAULT)
miniascape_DISK_5_QEMU_IMG_OPTS	?= $(miniascape_DISK_QEMU_IMG_OPTS_DEFAULT)

disk_opts	= --disk path=$(DISK_DIR)/$(miniascape_DISK_1_NAME),bus=$(miniascape_DISK_1_BUS),format=$(miniascape_DISK_1_FMT),perms=$(miniascape_DISK_1_PERMS),cache=$(miniascape_DISK_1_CACHE_MODE)
network_opts	= --network=$(miniascape_NETWORK_1),model=$(miniascape_NET_1_MODEL),mac=$(miniascape_MAC_1)


## disk images:
disk_images	= $(DISK_DIR)/$(miniascape_DISK_1_NAME)

$(DISK_DIR):
	mkdir -p $@

# There must be one disk image at least.
$(DISK_DIR)/$(miniascape_DISK_1_NAME): $(DISK_DIR)
	$(miniascape_QEMU_IMG) create -f $(miniascape_DISK_1_FMT) $(miniascape_DISK_1_QEMU_IMG_OPTS) $@ $(miniascape_DISK_1_SIZE)G


# Optional disk images
ifneq ($(miniascape_DISK_2_NAME),)
disk_images	+= $(DISK_DIR)/$(miniascape_DISK_2_NAME)
disk_opts	+= --disk path=$(DISK_DIR)/$(miniascape_DISK_2_NAME),bus=$(miniascape_DISK_2_BUS),format=$(miniascape_DISK_2_FMT),perms=$(miniascape_DISK_2_PERMS),cache=$(miniascape_DISK_2_CACHE_MODE)

$(DISK_DIR)/$(miniascape_DISK_2_NAME):
	$(miniascape_QEMU_IMG) create -f $(miniascape_DISK_2_FMT) $(miniascape_DISK_2_QEMU_IMG_OPTS) $@ $(miniascape_DISK_2_SIZE)G
endif
ifneq ($(miniascape_DISK_3_NAME),)
disk_images	+= $(DISK_DIR)/$(miniascape_DISK_3_NAME)
disk_opts	+= --disk path=$(DISK_DIR)/$(miniascape_DISK_3_NAME),bus=$(miniascape_DISK_3_BUS),format=$(miniascape_DISK_3_FMT),perms=$(miniascape_DISK_3_PERMS),cache=$(miniascape_DISK_3_CACHE_MODE)

$(DISK_DIR)/$(miniascape_DISK_3_NAME):
	$(miniascape_QEMU_IMG) create -f $(miniascape_DISK_3_FMT) $(miniascape_DISK_3_QEMU_IMG_OPTS) $@ $(miniascape_DISK_3_SIZE)G
endif
ifneq ($(DISK_4_NAME),)
disk_images	+= $(DISK_DIR)/$(miniascape_DISK_4_NAME)
disk_opts	+= --disk path=$(DISK_DIR)/$(miniascape_DISK_4_NAME),bus=$(miniascape_DISK_4_BUS),format=$(miniascape_DISK_4_FMT),perms=$(miniascape_DISK_4_PERMS),cache=$(miniascape_DISK_4_CACHE_MODE)

$(DISK_DIR)/$(miniascape_DISK_4_NAME):
	$(miniascape_QEMU_IMG) create -f $(miniascape_DISK_4_FMT) $(miniascape_DISK_4_QEMU_IMG_OPTS) $@ $(miniascape_DISK_4_SIZE)G
endif
ifneq ($(miniascape_DISK_5_NAME),)
disk_images	+= $(DISK_DIR)/$(miniascape_DISK_5_NAME)
disk_opts	+= --disk path=$(DISK_DIR)/$(miniascape_DISK_5_NAME),bus=$(miniascape_DISK_5_BUS),format=$(miniascape_DISK_5_FMT),perms=$(miniascape_DISK_5_PERMS),cache=$(miniascape_DISK_5_CACHE_MODE)

$(DISK_DIR)/$(miniascape_DISK_5_NAME):
	$(miniascape_QEMU_IMG) create -f $(miniascape_DISK_5_FMT) $(miniascape_DISK_5_QEMU_IMG_OPTS) $@ $(miniascape_DISK_5_SIZE)G
endif

# vim:set ft=make ai si sm:

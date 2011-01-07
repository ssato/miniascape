#
# lib. makefiles - disk (storage) stuff
#

ifeq ($(miniascape_DISK_1_NAME),)
$(error You must specify miniascape_DISK_1_NAME, that is, single disk is needed for a VM at least.)
endif

miniascape_DISK_SUBDIR	?= $(miniascape_NAME)

miniascape_DISK_1_SIZE	?= $(miniascape_DISK_SIZE)
miniascape_DISK_1_BUS	?= $(miniascape_DISK_BUS)
miniascape_DISK_1_PERMS	?= $(miniascape_DISK_PERMS)
miniascape_DISK_1_FMT	?= $(miniascape_DISK_IMG_FMT)
miniascape_DISK_1_NAME	?= disk-1.$(miniascape_DISK_IMG_FMT)
miniascape_DISK_1_CACHE_MODE ?= $(miniascape_DISK_CACHE_MODE)
miniascape_DISK_1_QEMU_IMG_OPTS	?= $(miniascape_DISK_QEMU_IMG_OPTS_DEFAULT)

DISK_DIR	= $(miniascape_DISK_TOPDIR)/$(miniascape_DISK_SUBDIR)
disk_images	= $(DISK_DIR)/$(miniascape_DISK_1_NAME)

#
# Temporal workaround for a bug in virt-install fixed at:
# http://hg.fedorahosted.org/hg/python-virtinst/rev/b2eec170e9fa
#
# NOTE: This will be eliminated after new version of python-virtinst contains
# the above fix.
#
ifeq ($(miniascape_DISK_1_PERMS),rw)
disk_opts	= --disk path=$(DISK_DIR)/$(miniascape_DISK_1_NAME),bus=$(miniascape_DISK_1_BUS),format=$(miniascape_DISK_1_FMT),cache=$(miniascape_DISK_1_CACHE_MODE)
else
disk_opts	= --disk path=$(DISK_DIR)/$(miniascape_DISK_1_NAME),bus=$(miniascape_DISK_1_BUS),format=$(miniascape_DISK_1_FMT),cache=$(miniascape_DISK_1_CACHE_MODE),perms=$(miniascape_DISK_1_PERMS)
endif

$(DISK_DIR):
	mkdir -p $@

$(DISK_DIR)/$(miniascape_DISK_1_NAME): $(DISK_DIR)
	$(miniascape_QEMU_IMG) create -f $(miniascape_DISK_1_FMT) $(miniascape_DISK_1_QEMU_IMG_OPTS) $@ $(miniascape_DISK_1_SIZE)


ifneq ($(miniascape_DISK_2_NAME),)
miniascape_DISK_2_SIZE     ?= $(miniascape_DISK_SIZE)
miniascape_DISK_2_BUS      ?= $(miniascape_DISK_BUS)
miniascape_DISK_2_PERMS	?= $(miniascape_DISK_PERMS)
miniascape_DISK_2_CACHE_MODE ?= $(miniascape_DISK_CACHE_MODE)
miniascape_DISK_2_FMT	?= $(miniascape_DISK_IMG_FMT)
miniascape_DISK_2_QEMU_IMG_OPTS	?= $(miniascape_DISK_QEMU_IMG_OPTS_DEFAULT)
miniascape_DISK_2_NAME     ?= disk-2.$(miniascape_DISK_IMG_FMT)

disk_2_perms_opt	= $(shell test "x$(miniascape_DISK_2_PERMS)" = "xrw" && echo "" || echo ,perms=$(miniascape_DISK_2_PERMS))

disk_images	+= $(DISK_DIR)/$(miniascape_DISK_2_NAME)
disk_opts	+= --disk path=$(DISK_DIR)/$(miniascape_DISK_2_NAME),bus=$(miniascape_DISK_2_BUS),format=$(miniascape_DISK_2_FMT),cache=$(miniascape_DISK_2_CACHE_MODE)$(disk_2_perms_opt)

$(DISK_DIR)/$(miniascape_DISK_2_NAME): $(DISK_DIR)
	$(miniascape_QEMU_IMG) create -f $(miniascape_DISK_2_FMT) $(miniascape_DISK_2_QEMU_IMG_OPTS) $@ $(miniascape_DISK_2_SIZE)
endif


ifneq ($(miniascape_DISK_3_NAME),)
miniascape_DISK_3_SIZE     ?= $(miniascape_DISK_SIZE)
miniascape_DISK_3_BUS      ?= $(miniascape_DISK_BUS)
miniascape_DISK_3_PERMS	?= $(miniascape_DISK_PERMS)
miniascape_DISK_3_CACHE_MODE ?= $(miniascape_DISK_CACHE_MODE)
miniascape_DISK_3_FMT	?= $(miniascape_DISK_IMG_FMT)
miniascape_DISK_3_QEMU_IMG_OPTS	?= $(miniascape_DISK_QEMU_IMG_OPTS_DEFAULT)
miniascape_DISK_3_NAME     ?= disk-3.$(miniascape_DISK_IMG_FMT)

disk_3_perms_opt	= $(shell test "x$(miniascape_DISK_3_PERMS)" = "xrw" && echo "" || echo ,perms=$(miniascape_DISK_3_PERMS))

disk_images	+= $(DISK_DIR)/$(miniascape_DISK_3_NAME)
disk_opts	+= --disk path=$(DISK_DIR)/$(miniascape_DISK_3_NAME),bus=$(miniascape_DISK_3_BUS),format=$(miniascape_DISK_3_FMT),cache=$(miniascape_DISK_3_CACHE_MODE)$(disk_3_perms_opt)

$(DISK_DIR)/$(miniascape_DISK_3_NAME): $(DISK_DIR)
	$(miniascape_QEMU_IMG) create -f $(miniascape_DISK_3_FMT) $(miniascape_DISK_3_QEMU_IMG_OPTS) $@ $(miniascape_DISK_3_SIZE)
endif


ifneq ($(miniascape_DISK_4_NAME),)
miniascape_DISK_4_SIZE     ?= $(miniascape_DISK_SIZE)
miniascape_DISK_4_BUS      ?= $(miniascape_DISK_BUS)
miniascape_DISK_4_PERMS	?= $(miniascape_DISK_PERMS)
miniascape_DISK_4_CACHE_MODE ?= $(miniascape_DISK_CACHE_MODE)
miniascape_DISK_4_FMT	?= $(miniascape_DISK_IMG_FMT)
miniascape_DISK_4_QEMU_IMG_OPTS	?= $(miniascape_DISK_QEMU_IMG_OPTS_DEFAULT)
miniascape_DISK_4_NAME     ?= disk-4.$(miniascape_DISK_IMG_FMT)

disk_4_perms_opt	= $(shell test "x$(miniascape_DISK_4_PERMS)" = "xrw" && echo "" || echo ,perms=$(miniascape_DISK_4_PERMS))

disk_images	+= $(DISK_DIR)/$(miniascape_DISK_4_NAME)
disk_opts	+= --disk path=$(DISK_DIR)/$(miniascape_DISK_4_NAME),bus=$(miniascape_DISK_4_BUS),format=$(miniascape_DISK_4_FMT),cache=$(miniascape_DISK_4_CACHE_MODE)$(disk_4_perms_opt)

$(DISK_DIR)/$(miniascape_DISK_4_NAME): $(DISK_DIR)
	$(miniascape_QEMU_IMG) create -f $(miniascape_DISK_4_FMT) $(miniascape_DISK_4_QEMU_IMG_OPTS) $@ $(miniascape_DISK_4_SIZE)
endif

# vim:set ft=make ai si sm:

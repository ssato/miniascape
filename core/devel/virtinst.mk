#
# lib. makefiles - virt-install related 
#

ifeq ($(miniascape_NAME),)
$(error You must specify miniascape_NAME)
endif
ifeq ($(miniascape_LOCATION),)
$(error You must specify miniascape_LOCATION)
endif
ifeq ($(miniascape_EXTRA_ARGS),)
$(error You must specify miniascape_EXTRA_ARGS)
endif


prebuild.stamp: $(disk_images)
	touch $@

build.stamp: build-vm
	touch $@

build-vm: prebuild.stamp
	$(miniascape_VIRTINST) --connect=$(miniascape_CONNECT) --name=$(miniascape_NAME) \
		--ram=$(miniascape_MEMORY) --arch=$(miniascape_ARCH) \
		--vcpu=$(miniascape_VCPU) --keymap=$(miniascape_KEYMAP) \
		--os-type=$(miniascape_OS_TYPE) \
		--location=$(miniascape_LOCATION) --os-variant=$(miniascape_OS_VARIANT) \
		$(disk_opts) \
		$(network_opts) \
		--extra-args=$(miniascape_EXTRA_ARGS) \
		$(miniascape_OTHER_OPTIONS) \
		$(NULL)

.PHONY: build-vm
# vim:set ft=make ai si sm:

prebuild.stamp: $(disk_images)

build.stamp: build-vm

build-vm: prebuild.stamp
	$(miniascape_VIRTINST) --connect=$(miniascape_CONNECT) --name=$(miniascape_NAME) \
		--ram=$(miniascape_MEMORY) --arch=$(miniascape_ARCH) \
		--vcpu=$(miniascape_VCPU) --keymap=$(miniascape_KEYMAP) \
		--os-type=$(miniascape_OS_TYPE) \
		--location=$(miniascape_LOCATION) --os-variant=$(miniascape_OS_VARIANT) \
		$(disk_opts) \
		$(network_opts) \
		--extra-args=$(miniascape_EXTRA_ARGS) \
		$(miniascape_INJECT_INITRD) \
		$(other_opts) \
		$(miniascape_OTHER_OPTIONS) \
		$(NULL)

.PHONY: build-vm
# vim:set ft=make ai si sm:

fenceconfdir = $(sysconfdir)/$(PACKAGE)/fence
fencekeydir = $(sysconfdir)/cluster

dist_fenceconf_DATA = fence_virt.conf
dist_fencekey_DATA = fence_xvm.key

fence_xvm.key:
	dd if=/dev/random bs=512 count=1 of=$@

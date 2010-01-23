SUBDIRS	= init sysconfig

dist_fencedkeydata_DATA	= fence_xvm.key
fencedkeydatadir	= @sysconfdir@/cluster

fence_xvm.key:
	dd if=/dev/urandom of=$@ bs=4k count=1


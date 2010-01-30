fencedsysconfdir	= @sysconfdir@/sysconfig
fencedkeydatadir        = @sysconfdir@/cluster
dist_fencedsysconf_DATA	= fence_xvmd
dist_fencedkeydata_DATA = fence_xvm.key

fence_xvm.key:
	dd if=/dev/urandom of=$@ bs=4k count=1


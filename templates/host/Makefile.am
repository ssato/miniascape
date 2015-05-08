EXTRA_DIST = package.spec rpm.mk
include $(abs_top_srcdir)/rpm.mk

pkgdata0dir = /usr/share/libvirt/networks
dist_pkgdata0_DATA = $(wildcard networks/*.xml)

pkgdata1dir = /usr/libexec/miniascape
dist_pkgdata1_DATA = \
usr/libexec/miniascape/register_libvirt_network.sh \
usr/libexec/miniascape/guest_network_register.sh

pkgdata2dir = /usr/libexec/miniascape/default
dist_pkgdata2_DATA = \
usr/libexec/miniascape/default/create_lio_iscsi_lun.sh \
usr/libexec/miniascape/default/fixup_software_bridge.sh

pkgdata3dir = /etc
dist_pkgdata3_DATA = \
etc/fence_virt.conf

pkgdata6dir = /etc/modprobe.d
dist_pkgdata6_DATA = \
etc/modprobe.d/kvm.conf

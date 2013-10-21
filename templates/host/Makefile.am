EXTRA_DIST = {{ name|default('miniascape-host-data-default') }}.spec rpm.mk
include $(abs_top_srcdir)/rpm.mk

pkgdata0dir = /usr/share/miniascape/networks.d
dist_pkgdata0_DATA = \
usr/share/miniascape/networks.d/default.xml \
usr/share/miniascape/networks.d/openstack-private.xml \
usr/share/miniascape/networks.d/service.xml

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
etc/auto.isos \
etc/fence_virt.conf

pkgdata4dir = /etc/auto.master.d
dist_pkgdata4_DATA = \
etc/auto.master.d/isos.autofs

pkgdata5dir = /etc/httpd/conf.d
dist_pkgdata5_DATA = \
etc/httpd/conf.d/miniascape_autoinst.conf

pkgdata6dir = /etc/modprobe.d
dist_pkgdata6_DATA = \
etc/modprobe.d/kvm.conf

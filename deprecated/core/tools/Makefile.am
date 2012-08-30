pkglibexecdir = @libexecdir@/@PACKAGE@

nodist_pkglibexec_SCRIPTS = \
create-iscsi-disk-image \
net-manage-all \
virt-net-register \
virt-net-unregister \
resolve-vm-addr \
$(NULL)

CLEANFILES = $(nodist_pkglibexec_SCRIPTS)
EXTRA_DIST = $(addsuffix .in,$(nodist_pkglibexec_SCRIPTS))

subst	= $(AM_V_GEN)$(SED) -e 's,[@]pkgsysconfdir[@],$(sysconfdir)/$(PACKAGE),g' -e 's,[@]pkglibexecdir[@],$(pkglibexecdir),g' -e 's,[@]VIRSH[@],$(VIRSH),g' $(srcdir)/$< > $@.t && mv $@.t $@

create-iscsi-disk-image: create-iscsi-disk-image.in
	$(subst)

net-manage-all: net-manage-all.in
	$(subst)

virt-net-register: virt-net-register.in
	$(subst)

virt-net-unregister: virt-net-unregister.in
	$(subst)

resolve-vm-addr: resolve-vm-addr.in
	$(subst)

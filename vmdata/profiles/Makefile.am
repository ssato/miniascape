vmsysconfdir = @sysconfdir@/@BASE_PACKAGE@/profiles

dist_vmsysconf_DATA = \
site.cfg \
rhel-3-0-vm-1.cfg rhel-3-1-vm-1.cfg rhel-3-2-vm-1.cfg \
rhel-3-3-vm-1.cfg rhel-3-4-vm-1.cfg rhel-3-5-vm-1.cfg \
rhel-3-6-vm-1.cfg rhel-3-7-vm-1.cfg rhel-3-8-vm-1.cfg \
rhel-3-9-vm-1.cfg \
rhel-4-0-vm-1.cfg rhel-4-1-vm-1.cfg rhel-4-2-vm-1.cfg \
rhel-4-3-vm-1.cfg rhel-4-4-vm-1.cfg rhel-4-5-vm-1.cfg \
rhel-4-6-vm-1.cfg rhel-4-7-vm-1.cfg rhel-4-8-vm-1.cfg \
rhel-5-0-vm-1.cfg rhel-5-1-vm-1.cfg rhel-5-2-vm-1.cfg \
rhel-5-3-vm-1.cfg rhel-5-4-vm-1.cfg rhel-5-5-vm-1.cfg \
rhel-6-0-vm-1.cfg \
fedora-13-vm-1.cfg fedora-14-vm-1.cfg \
debian-0.cfg \
ubuntu-0.cfg \
rhel-5-luci-0.cfg rhel-5-cluster-1.cfg rhel-5-cluster-2.cfg \
rhel-5-cluster-3.cfg rhel-5-cluster-4.cfg rhel-5-cluster-5.cfg \
rhel-5-mrg-0.cfg rhel-5-mrg-1.cfg rhel-5-mrg-2.cfg \
rhel-5-mrg-3.cfg rhel-5-mrg-4.cfg  rhel-5-mrg-5.cfg  \
rhel-5-satellite-0.cfg rhel-5-satellite-1.cfg \
jon-0.cfg jon-1.cfg \
jboss-0.cfg jboss-1.cfg jboss-2.cfg jboss-3.cfg jboss-4.cfg jboss-5.cfg


fedora-13-vm-1.cfg: fedora-14-vm-1.cfg
	$(AM_V_GEN)$(SED) -e 's,fedora-14,fedora-13-1,g' -e 's,Fedora/14,Fedora/13,g' -e 's,fedora14,fedora13,g' \
		-e 's,:01:84,:01:83,g' -e 's,_PREFIX).184,_PREFIX).183,g' $(srcdir)/$< > $@.t && mv $@.t $@

jboss-1.cfg: jboss-0.cfg
	$(AM_V_GEN)$(SED) -e 's/jboss-0/jboss-1/g' -e 's/PREFIX).30/PREFIX).31/g' -e 's/:00:30/00:31/g' $(srcdir)/$< > $@.t && mv $@.t $@

jboss-2.cfg: jboss-0.cfg
	$(AM_V_GEN)$(SED) -e 's/jboss-0/jboss-2/g' -e 's/PREFIX).30/PREFIX).32/g' -e 's/:00:30/00:32/g' $(srcdir)/$< > $@.t && mv $@.t $@

jboss-3.cfg: jboss-0.cfg
	$(AM_V_GEN)$(SED) -e 's/jboss-0/jboss-3/g' -e 's/PREFIX).30/PREFIX).33/g' -e 's/:00:30/00:33/g' $(srcdir)/$< > $@.t && mv $@.t $@

jboss-4.cfg: jboss-0.cfg
	$(AM_V_GEN)$(SED) -e 's/jboss-0/jboss-4/g' -e 's/PREFIX).30/PREFIX).34/g' -e 's/:00:30/00:34/g' $(srcdir)/$< > $@.t && mv $@.t $@

jboss-5.cfg: jboss-0.cfg
	$(AM_V_GEN)$(SED) -e 's/jboss-0/jboss-5/g' -e 's/PREFIX).30/PREFIX).35/g' -e 's/:00:30/00:35/g' $(srcdir)/$< > $@.t && mv $@.t $@

jon-1.cfg: jon-0.cfg
	$(AM_V_GEN)$(SED) -e 's/jon-0/jon-1/g' -e 's/PREFIX).27/PREFIX).28/g' -e 's/:00:27/:00:29/g' $(srcdir)/$< > $@.t && mv $@.t $@

rhel-5-mrg-1.cfg: rhel-5-mrg-0.cfg
	$(AM_V_GEN)$(SED) -e 's/rhel-5-mrg-0/rhel-5-mrg-1/g' -e 's/PREFIX).80/PREFIX).81/g' -e 's/:00:80/00:81/g' $(srcdir)/$< > $@.t && mv $@.t $@

rhel-5-mrg-2.cfg: rhel-5-mrg-0.cfg
	$(AM_V_GEN)$(SED) -e 's/rhel-5-mrg-0/rhel-5-mrg-2/g' -e 's/PREFIX).80/PREFIX).82/g' -e 's/:00:80/00:82/g' $(srcdir)/$< > $@.t && mv $@.t $@

rhel-5-mrg-3.cfg: rhel-5-mrg-0.cfg
	$(AM_V_GEN)$(SED) -e 's/rhel-5-mrg-0/rhel-5-mrg-3/g' -e 's/PREFIX).80/PREFIX).83/g' -e 's/:00:80/00:83/g' $(srcdir)/$< > $@.t && mv $@.t $@

rhel-5-mrg-4.cfg: rhel-5-mrg-0.cfg
	$(AM_V_GEN)$(SED) -e 's/rhel-5-mrg-0/rhel-5-mrg-4/g' -e 's/PREFIX).80/PREFIX).84/g' -e 's/:00:80/00:84/g' $(srcdir)/$< > $@.t && mv $@.t $@

rhel-5-mrg-5.cfg: rhel-5-mrg-0.cfg
	$(AM_V_GEN)$(SED) -e 's/rhel-5-mrg-0/rhel-5-mrg-5/g' -e 's/PREFIX).80/PREFIX).85/g' -e 's/:00:80/00:85/g' $(srcdir)/$< > $@.t && mv $@.t $@


rhel-5-satellite-1.cfg: rhel-5-satellite-0.cfg
	$(AM_V_GEN)$(SED) -e 's/rhel-5-satellite-0/rhel-5-satellite-1/g' -e 's/PREFIX).20/PREFIX).21/g' -e 's/:00:20/00:21/g' $(srcdir)/$< > $@.t && mv $@.t $@

rhel-5-cluster-2.cfg: rhel-5-cluster-1.cfg
	$(AM_V_GEN)$(SED) -e 's/cluster-1/cluster-2/g' -e 's/PREFIX).51/PREFIX).52/g' -e 's/:00:51/:00:52/g' $(srcdir)/$< > $@.t && mv $@.t $@

rhel-5-cluster-3.cfg: rhel-5-cluster-1.cfg
	$(AM_V_GEN)$(SED) -e 's/cluster-1/cluster-3/g' -e 's/PREFIX).51/PREFIX).53/g' -e 's/:00:51/:00:53/g' $(srcdir)/$< > $@.t && mv $@.t $@

rhel-5-cluster-4.cfg: rhel-5-cluster-1.cfg
	$(AM_V_GEN)$(SED) -e 's/cluster-1/cluster-4/g' -e 's/PREFIX).51/PREFIX).54/g' -e 's/:00:51/:00:54/g' $(srcdir)/$< > $@.t && mv $@.t $@

rhel-5-cluster-5.cfg: rhel-5-cluster-1.cfg
	$(AM_V_GEN)$(SED) -e 's/cluster-1/cluster-5/g' -e 's/PREFIX).51/PREFIX).55/g' -e 's/:00:51/:00:55/g' $(srcdir)/$< > $@.t && mv $@.t $@



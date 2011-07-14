autoinstdatadir	= $(datadir)/$(PACKAGE)/autoinst
autoinstdata2dir	= $(autoinstdatadir)

dist_autoinstdata_DATA = \
fedora-13-i386-min.ks.cfg \
fedora-14-i386-min.ks.cfg \
debian-squeeze-preseed.cfg \
ubuntu-10.04-preseed.cfg \
rhel-6-0-i386-min.ks.cfg \
rhel-6-1-x86_64-min.ks.cfg \
rhel-6-cluster.ks.cfg \
rhel-5-cluster.ks.cfg \
rhel-6-satellite.ks.cfg \
rhel-5-satellite.ks.cfg \
rhel-5-mrg.ks.cfg \
rhel-5-jboss.ks.cfg \
rhel-5-luci.ks.cfg \
rhel-5-0-i386-min.ks.cfg \
rhel-4-0-i386-min.ks.cfg \
rhel-3-0-i386-min.ks.cfg \
rhel-3-2-i386-min.ks.cfg \
rhel-3-0-i386-default.ks.cfg \
rhel-3-2-i386-default.ks.cfg \
$(NULL)

nodist_autoinstdata2_DATA = \
rhel-5-1-i386-min.ks.cfg \
rhel-5-2-i386-min.ks.cfg \
rhel-5-3-i386-min.ks.cfg \
rhel-5-4-i386-min.ks.cfg \
rhel-5-5-i386-min.ks.cfg \
rhel-5-6-i386-min.ks.cfg \
rhel-4-1-i386-min.ks.cfg \
rhel-4-2-i386-min.ks.cfg \
rhel-4-3-i386-min.ks.cfg \
rhel-4-4-i386-min.ks.cfg \
rhel-4-5-i386-min.ks.cfg \
rhel-4-6-i386-min.ks.cfg \
rhel-4-7-i386-min.ks.cfg \
rhel-4-8-i386-min.ks.cfg \
rhel-3-1-i386-min.ks.cfg \
rhel-3-3-i386-min.ks.cfg \
rhel-3-4-i386-min.ks.cfg \
rhel-3-5-i386-min.ks.cfg \
rhel-3-6-i386-min.ks.cfg \
rhel-3-7-i386-min.ks.cfg \
rhel-3-8-i386-min.ks.cfg \
rhel-3-9-i386-min.ks.cfg \
rhel-3-1-i386-default.ks.cfg \
rhel-3-3-i386-default.ks.cfg \
rhel-3-4-i386-default.ks.cfg \
rhel-3-5-i386-default.ks.cfg \
rhel-3-6-i386-default.ks.cfg \
rhel-3-7-i386-default.ks.cfg \
rhel-3-8-i386-default.ks.cfg \
rhel-3-9-i386-default.ks.cfg \
rhel-4-0-i386-default.ks.cfg \
rhel-4-1-i386-default.ks.cfg \
rhel-4-2-i386-default.ks.cfg \
rhel-4-3-i386-default.ks.cfg \
rhel-4-4-i386-default.ks.cfg \
rhel-4-5-i386-default.ks.cfg \
rhel-4-6-i386-default.ks.cfg \
rhel-4-7-i386-default.ks.cfg \
rhel-4-8-i386-default.ks.cfg \
$(NULL)

EXTRA_DIST = \
rhel-3-0-i386-default.ks.cfg.in \
rhel-3-0-i386-min.ks.cfg.in \
rhel-3-2-i386-default.ks.cfg.in \
rhel-3-2-i386-min.ks.cfg.in \
rhel-4-0-i386-default.ks.cfg.in \
rhel-4-0-i386-min.ks.cfg.in \
rhel-5-0-i386-min.ks.cfg.in \
rhel-5-cluster.ks.cfg.in \
rhel-5-jboss.ks.cfg.in \
rhel-5-mrg.ks.cfg.in \
rhel-5-luci.ks.cfg.in \
rhel-5-satellite.ks.cfg.in \
rhel-6-cluster.ks.cfg.in \
rhel-6-satellite.ks.cfg.in \
rhel-6-0-i386-min.ks.cfg.in \
rhel-6-1-x86_64-min.ks.cfg.in \
$(NULL)

DISTCLEANFILES	= $(nodist_autoinstdata2_DATA)


# rhel 5 server i386, minimal packages
rhel-5-1-i386-min.ks.cfg: rhel-5-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/5/0/,rhel/5/1/,g' $< > $@

rhel-5-2-i386-min.ks.cfg: rhel-5-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/5/0/,rhel/5/2/,g' $< > $@

rhel-5-3-i386-min.ks.cfg: rhel-5-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/5/0/,rhel/5/3/,g' $< > $@

rhel-5-4-i386-min.ks.cfg: rhel-5-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/5/0/,rhel/5/4/,g' $< > $@

rhel-5-5-i386-min.ks.cfg: rhel-5-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/5/0/,rhel/5/5/,g' $< > $@

rhel-5-6-i386-min.ks.cfg: rhel-5-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/5/0/,rhel/5/6/,g' $< > $@


# rhel 4 as i386, minimal packages
rhel-4-1-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/1/,' $< > $@

rhel-4-2-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/2/,' $< > $@

rhel-4-3-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/3/,' $< > $@

rhel-4-4-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/4/,' $< > $@

rhel-4-5-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/5/,' $< > $@

rhel-4-6-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/6/,' $< > $@

rhel-4-7-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/7/,' $< > $@

rhel-4-8-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/8/,' $< > $@

# rhel 4 as i386, default packages
rhel-4-1-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/1/,' $< > $@

rhel-4-2-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/2/,' $< > $@

rhel-4-3-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/3/,' $< > $@

rhel-4-4-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/4/,' $< > $@

rhel-4-5-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/5/,' $< > $@

rhel-4-6-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/6/,' $< > $@

rhel-4-7-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/7/,' $< > $@

rhel-4-8-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/4/0/,rhel/4/8/,' $< > $@


# rhel 3 as i386, default packages
rhel-3-1-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/1/,' $< > $@

# Special case: anaconda in rhel-3-2 does not like --port option for firewall
# command. So custom ks.cfg is required for this version.

rhel-3-3-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/3/,' $< > $@

rhel-3-4-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/4/,' $< > $@

rhel-3-5-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/5/,' $< > $@

rhel-3-6-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/6/,' $< > $@

rhel-3-7-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/7/,' $< > $@

rhel-3-8-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/8/,' $< > $@

rhel-3-9-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/9/,' $< > $@

# rhel 3 as i386, minimal packages
rhel-3-1-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/1/,' $< > $@

# See above comment. 
#rhel-3-2-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
#	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/2/,' $< > $@

rhel-3-3-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/3/,' $< > $@

rhel-3-4-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/4/,' $< > $@

rhel-3-5-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/5/,' $< > $@

rhel-3-6-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/6/,' $< > $@

rhel-3-7-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/7/,' $< > $@

rhel-3-8-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/8/,' $< > $@

rhel-3-9-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	$(AM_V_GEN)$(SED) -e 's,rhel/3/0/,rhel/3/9/,' $< > $@



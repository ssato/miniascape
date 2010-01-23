kscfgdatadir = @datadir@/@PACKAGE@/kickstart

dist_kscfgdata_DATA = \
rhel-6-0-i386-min.ks.cfg \
rhel-5-satellite.ks.cfg \
rhel-5-0-i386-min.ks.cfg \
rhel-5-1-i386-min.ks.cfg \
rhel-5-2-i386-min.ks.cfg \
rhel-5-3-i386-min.ks.cfg \
rhel-5-4-i386-min.ks.cfg \
rhel-4-0-i386-min.ks.cfg \
rhel-4-1-i386-min.ks.cfg \
rhel-4-2-i386-min.ks.cfg \
rhel-4-3-i386-min.ks.cfg \
rhel-4-4-i386-min.ks.cfg \
rhel-4-5-i386-min.ks.cfg \
rhel-4-6-i386-min.ks.cfg \
rhel-4-7-i386-min.ks.cfg \
rhel-4-8-i386-min.ks.cfg \
rhel-3-0-i386-min.ks.cfg \
rhel-3-1-i386-min.ks.cfg \
rhel-3-2-i386-min.ks.cfg \
rhel-3-3-i386-min.ks.cfg \
rhel-3-4-i386-min.ks.cfg \
rhel-3-5-i386-min.ks.cfg \
rhel-3-6-i386-min.ks.cfg \
rhel-3-7-i386-min.ks.cfg \
rhel-3-8-i386-min.ks.cfg \
rhel-3-9-i386-min.ks.cfg \
rhel-3-0-i386-default.ks.cfg \
rhel-3-1-i386-default.ks.cfg \
rhel-3-2-i386-default.ks.cfg \
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
rhel-4-8-i386-default.ks.cfg

## FIXME: It doesn't work.
# Needs installation key.
#ifdef $(RHEL_INSTALLATION_KEY)
#dist_kscfgdata_DATA += rhel-5-cluster.ks.cfg
#endif


# rhel 5 server i386, minimal packages
rhel-5-1-i386-min.ks.cfg: rhel-5-0-i386-min.ks.cfg
	sed -e 's,RHEL/5/0/i386,RHEL/5/1/i386,g' $< > $@

rhel-5-2-i386-min.ks.cfg: rhel-5-0-i386-min.ks.cfg
	sed -e 's,RHEL/5/0/i386,RHEL/5/2/i386,g' $< > $@

rhel-5-3-i386-min.ks.cfg: rhel-5-0-i386-min.ks.cfg
	sed -e 's,RHEL/5/0/i386,RHEL/5/3/i386,g' $< > $@

rhel-5-4-i386-min.ks.cfg: rhel-5-0-i386-min.ks.cfg
	sed -e 's,RHEL/5/0/i386,RHEL/5/4/i386,g' $< > $@


# rhel 4 as i386, minimal packages
rhel-4-1-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/1/i386,' $< > $@

rhel-4-2-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/2/i386,' $< > $@

rhel-4-3-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/3/i386,' $< > $@

rhel-4-4-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/4/i386,' $< > $@

rhel-4-5-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/5/i386,' $< > $@

rhel-4-6-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/6/i386,' $< > $@

rhel-4-7-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/7/i386,' $< > $@

rhel-4-8-i386-min.ks.cfg: rhel-4-0-i386-min.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/8/i386,' $< > $@

# rhel 4 as i386, default packages
rhel-4-1-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/1/i386,' $< > $@

rhel-4-2-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/2/i386,' $< > $@

rhel-4-3-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/3/i386,' $< > $@

rhel-4-4-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/4/i386,' $< > $@

rhel-4-5-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/5/i386,' $< > $@

rhel-4-6-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/6/i386,' $< > $@

rhel-4-7-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/7/i386,' $< > $@

rhel-4-8-i386-default.ks.cfg: rhel-4-0-i386-default.ks.cfg
	sed -e 's,RHEL/4/0/i386,RHEL/4/8/i386,' $< > $@


# rhel 3 as i386, default packages
rhel-3-1-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/1/i386,' $< > $@

# Special case: anaconda in rhel-3-2 does not like --port option for firewall
# command. So custom ks.cfg is required for this version.
#rhel-3-2-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
#	sed -e 's,RHEL/3/0/i386,RHEL/3/2/i386,' $< > $@

rhel-3-3-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/3/i386,' $< > $@

rhel-3-4-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/4/i386,' $< > $@

rhel-3-5-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/5/i386,' $< > $@

rhel-3-6-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/6/i386,' $< > $@

rhel-3-7-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/7/i386,' $< > $@

rhel-3-8-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/8/i386,' $< > $@

rhel-3-9-i386-default.ks.cfg: rhel-3-0-i386-default.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/9/i386,' $< > $@

# rhel 3 as i386, minimal packages
rhel-3-1-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/1/i386,' $< > $@

# See above comment. 
#rhel-3-2-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
#	sed -e 's,RHEL/3/0/i386,RHEL/3/2/i386,' $< > $@

rhel-3-3-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/3/i386,' $< > $@

rhel-3-4-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/4/i386,' $< > $@

rhel-3-5-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/5/i386,' $< > $@

rhel-3-6-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/6/i386,' $< > $@

rhel-3-7-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/7/i386,' $< > $@

rhel-3-8-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/8/i386,' $< > $@

rhel-3-9-i386-min.ks.cfg: rhel-3-0-i386-min.ks.cfg
	sed -e 's,RHEL/3/0/i386,RHEL/3/9/i386,' $< > $@


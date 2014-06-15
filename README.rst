============
miniascape
============

Disclaimer
-----------

WARNING: miniascape is in pre-alpha state and will heavily udpate day by day,
so it may not work in your environment or might cause trouble. TRY IT IN YOUR
OWN RISK, PLEASE.

About
-------

Miniascape is a template compiler optimized for specific purpose to generate
collection of configuration files for virt. host, script to build VMs, and misc
data for VMs, to setup libvirt based virtualization environment (virtualization
'miniascape') to build VMs quickly and easily.

Main objects are

* Setup network configuration including DHCP and DNS for VMs much easier.

* Lightweight; Does not require expensive high-performance servers.
  
  I try to make it working on my non-high power vaio note pc having Intel Atom
  CPU and only 2G RAM.

* Fully utilize exsiting library, tools and do not intend to replace or
  reinvent wheels.

* Do not bring yet-another runtime dependency other than existing ones
  like libvirt and virt-install and miniascape trys to generate scripts
  utilizing these and runnable standalone.

And non-goals are:

* Intend to become a replacement for other feature rich software such like
  RHEV, RHN Satellite and cobbler, CloudForms/SystemEngine, etc.

* Provides a UI (GUI, Web UI) to manage lifecycle of VMs at ease.
* Provides a CLI interface wraps exsiting tools and forcing users to learn new
  its way like vagrant

Usage
========

1. Setup host: mount iso images and setup kickstart installation trees, etc.
2. Arrange configuration files as needed. For example,

   - Just use default config files provided in this dist by specifying the path
     selected from /etc/miniascape.d/{default,openstack,rhui} with -C/--ctx
     option later on build.

   - Use default (select from /etc/miniascape.d/{default,openstack,rhui} ) and
     your custom ones, e.g. ./conf/custom/\*.yml.

   - Use your custom ones; make custom config files based on the default ones.

3. Run miniascape to configure and build libvirt network xml, auto installation
   script and vm build scripts. For examples,

   - miniascape -C /etc/miniascape.d/default b -w /tmp/workdir
   - miniascape -C /etc/miniascape.d/default -C myconf.d/ b -w /tmp/workdir
   - miniascape -C myconf.d/\*.yml b -w /tmp/workdir

   see the outoutpu of 'miniascape b --help' for more about its options.

4. Transfer outputs to your target libvirt host and run vm build script in the
   working dir (<workdir>/guests.d/<guest_name>/vmbuild.sh) on that host

How it works?
==============

Miniascape is just a template compiler optimized to generate ks.cfg, wrapper
scripts around virt-install and configurations installed into the libvirt host
in current implementation.

* Inputs: multiple YAML configuration files and template files specified in
  config (context) files with -C/--ctx options

* Outputs: libvirt network XML, kickstart files and VM build scripts, etc.
* Template engine used: Jinja2: http://jinja.pocoo.org

Configurations
----------------

Configurations and parameters are in YAML configuration files (default:
/etc/miniascape.d/default/\*.yml) or any other formats anyconfig module can
load (you have to specify glob patterns in this case, e.g. -C
/path/to/conf/\*.json).

Miniascape will load these config files, merge configurations in these files
and dump multiple intermediate configuration files ('configure' process) in
working dir specified with -w/--workdir option.

Intermediate config files are:

* Common: common/\*.yml
* Host global:

  * host.d/\*.yml
  * networks.d/\*.yml: Libvirt network parameters

* VM (guest) specific:

  1. guests.d/<guest group>/\*.yml: Parameters common in system groups
  2. guests.d/<guest group>/<guest name>/\*.yml: Guest specific parameters

And these configuration files are loaded in the above order and possible to
customize by putting your configuration files by hand.

And then miniascape will load these intermediate config files and templates,
and dump result files (ks.cfg, vm build scripts, etc.) under working dir.

Templates
----------

I chose jinja2 as template engine for miniascape.

Miniascape contains some concrete template examples under
/usr/share/miniascape/templates:

* autoinstall.d/: Auto installation configuration files (kickstart) templates
* host/: Templates for host like network xml, wrapper script for virt-install

Prerequisites
==============

Hardware and base OS
----------------------

* Intel x86 (i386 or x86_64) machine with VT extension (Intel VT or AMD-V) enabled
* RHEL 6 or Fedora 13+ or any linux distributions corresponding to these versions

Tools and libs
-------------------

 * libvirt and its python binding
 * python-virtinst
 * python-anyconfig: https://pypi.python.org/pypi/anyconfig/ or https://github.com/ssato/python-anyconfig
 * qemu-kvm
 * nginx or (apache) httpd [option]
 * etc.

Build
========

Run `python setup.py srpm` and mock dist/SRPMS/<built-srpm>, or 
run `python setup.py rpm`.

Installation
=============

* [Recommended] build srpm, rpm w/ mock and install it
* build and install: `python setup.py build` and `python setup.py install`

TODO
======

Upstream works
----------------

* --config (or --profile?) file option for virt-install [Should]
* more D-Bus APIs for dnsmasq to simplify the control process of dnsmasq and
  make it dynamic [May]

* It seems that virt-install do not create storage volumes on demand [Should]:

  ::

    [root@lp5-4 out]# bash -x ../miniascape/guests.d/rhel-5-cluster-1/vmbuild.sh
    + set -ex
    + test 0 -gt 0
    + ks_path=../miniascape/guests.d/rhel-5-cluster-1/ks.cfg
    + kscfg=ks.cfg
    + name=rhel-5-cluster-1
    + location_opts='--location=http://xxxxx.redhat.com/contents/RHEL/5/10/x86_64/default/ --initrd-inject=../miniascape/guests.d/rhel-5-cluster-1/ks.cfg'
    + ksdevice=eth0
    + more_extra_args=
    + virtio_scsi_controller=
    + virt-install --check-cpu --hvm --accelerate --noreboot --noautoconsole --name=rhel-5-cluster-1 --connect=qemu:///system --wait=12 --ram=512 --arch=x86_64 --vcpus=1 --graphics vnc --os-type=linux --os-variant=rhel5.4 --location=http://xxxxxx.redhat.com/contents/RHEL/5/10/x86_64/default/ --initrd-inject=../miniascape/guests.d/rhel-5-cluster-1/ks.cfg '--extra-args=ks=file:/ks.cfg ksdevice=eth0 ' --disk pool=default,format=qcow2,cache=none,size=5,bus=virtio --disk vol=default/rhel-5-cluster-data-1.img,format=qcow2,cache=none,size=1,bus=virtio,perms=sh --network network=service,model=virtio,mac=52:54:00:05:01:01 --network network=default,model=virtio,mac=52:54:00:02:01:01
    ERROR    Error with storage parameters: Couldn't lookup volume object: Storage volume not found: no storage vol with matching name 'rhel-5-cluster-data-1.img'
    [root@lp5-4 out]#


Done:

* python-virtinst (virt-install) fixes and enhancements:

  * perms=rw storage option is not handled correctly: my patch was merged.
  * Fix a bug that multiple storage volume cannot be created in a same storage
    pool with virt-install --disk option (rhbz#857424): My patch was merged.

* libvirt fixes and enhancements:

  * Implement dnsmasq backend for libvirt: My patch was merged.

miniascape itself
-------------------

* Some more guest configurations and templates
* Refine and enhance bootstrap process
* Implement a kind of template test framework and add some more tests around them
* Write unit tests for template files including snippets
* Added some more host-configuration stuff, like autofs, www (apache or nginx),
  nfs, iscsi, pxe boot, etc.
* Documents

Done:

* Simplify the process to generate intermediate config files and re-organize sub commands
* Utilize python-anyconfig to stack config files
* control or meta config file which controls which config files to be loaded

License
=========

This is distributed under GPLv3 or later.

Author
========

Satoru SATOH <ssato at redhat.com>

EXAMPLE Session
=================

::

  ssato@localhost% miniascape                      ~/repos/public/github.com/ssato/miniascape.git
  Usage: /usr/bin/miniascape COMMAND_OR_COMMAND_ALIAS [Options] [Arg ...]

  Commands:
          bootstrap (alias: bo)   Bootstrap site config files from ctx src and conf templates
          build (alias: b)        build (generate) outputs from tempaltes and context files
          configure (alias: c)    Same as the above ('build')

  ssato@localhost% miniascape b -h                 ~/repos/public/github.com/ssato/miniascape.git
  Usage: miniascape [OPTION ...]

  Options:
    -h, --help            show this help message and exit
    -t TMPLDIR, --tmpldir=TMPLDIR
                          Template top dir[s]
                          [[/usr/share/miniascape/templates]]
    -s SITE, --site=SITE  Choose site [default]
    -C CTX, --ctx=CTX     Specify context (conf) file[s] or path glob pattern or
                          dir (*.yml will be searched). It can be given multiple
                          times to specify multiple ones, ex. -C /a/b/c.yml -C
                          '/a/d/*.yml' -C /a/e/ [/etc/miniascape.d/<site>]. This
                          option is only supported in some sub commands,
                          configure and bootstrap.
    -w WORKDIR, --workdir=WORKDIR
                          Working dir to output results [miniascape-
                          workdir-20140612]
    -v, --verbose         Verbose mode
    -q, --quiet           Quiet mode
    --no-build            Do not build, generate ks.cfg, vm build scripts, etc.
    --no-genconf          Do not generate config from context files
  ssato@localhost% miniascape b -C conf/default -w /tmp/w
  2014-06-12 02:39:02,433 anyconfig: [INFO] Loading: /etc/miniascape.d/default/00_base.yml
  2014-06-12 02:39:02,450 anyconfig: [INFO] Loading: /etc/miniascape.d/default/02_host.yml
  2014-06-12 02:39:02,462 anyconfig: [INFO] Loading: /etc/miniascape.d/default/10_networks.yml
  2014-06-12 02:39:02,469 anyconfig: [INFO] Loading: /etc/miniascape.d/default/15_guests.yml
  2014-06-12 02:39:02,635 anyconfig: [INFO] Loading: conf/default/00_base.yml
  2014-06-12 02:39:02,649 anyconfig: [INFO] Loading: conf/default/02_host.yml
  2014-06-12 02:39:02,659 anyconfig: [INFO] Loading: conf/default/10_networks.yml
  2014-06-12 02:39:02,667 anyconfig: [INFO] Loading: conf/default/15_guests.yml
  2014-06-12 02:39:02,830 miniascape: [INFO] Generating site config files into /tmp/w/default
  2014-06-12 02:39:02,830 anyconfig: [INFO] Dumping: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:02,839 anyconfig: [INFO] Dumping: /tmp/w/default/host.d/00_base.yml
  2014-06-12 02:39:02,856 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/ipa/00_base.yml
  2014-06-12 02:39:02,859 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/ipa/ipa-1/00_base.yml
  2014-06-12 02:39:02,861 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/jboss/00_base.yml
  2014-06-12 02:39:02,865 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/jboss/jboss-0/00_base.yml
  2014-06-12 02:39:02,868 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/jboss/jboss-1/00_base.yml
  2014-06-12 02:39:02,869 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/jboss/jboss-2/00_base.yml
  2014-06-12 02:39:02,871 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/jboss/jboss-3/00_base.yml
  2014-06-12 02:39:02,872 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/jboss/jboss-4/00_base.yml
  2014-06-12 02:39:02,874 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhds/00_base.yml
  2014-06-12 02:39:02,876 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhds/rhds-1/00_base.yml
  2014-06-12 02:39:02,877 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-5-client/00_base.yml
  2014-06-12 02:39:02,879 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-5-client/rhel-5-client-1/00_base.yml
  2014-06-12 02:39:02,880 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-5-client/rhel-5-client-2/00_base.yml
  2014-06-12 02:39:02,881 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-5-cluster/00_base.yml
  2014-06-12 02:39:02,885 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-5-cluster/rhel-5-cluster-1/00_base.yml
  2014-06-12 02:39:02,888 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-5-cluster/rhel-5-cluster-2/00_base.yml
  2014-06-12 02:39:02,890 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-mrg-m/00_base.yml
  2014-06-12 02:39:02,892 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-mrg-m/rhel-6-mrg-m-1/00_base.yml
  2014-06-12 02:39:02,893 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-mrg-m/rhel-6-mrg-m-2/00_base.yml
  2014-06-12 02:39:02,895 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-client/00_base.yml
  2014-06-12 02:39:02,896 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-client/rhel-6-client-1/00_base.yml
  2014-06-12 02:39:02,897 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-cluster-gfs/00_base.yml
  2014-06-12 02:39:02,906 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-cluster-gfs/rhel-6-cluster-gfs-1/00_base.yml
  2014-06-12 02:39:02,910 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-cluster-gfs/rhel-6-cluster-gfs-2/00_base.yml
  2014-06-12 02:39:02,913 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-cluster-gfs/rhel-6-cluster-gfs-3/00_base.yml
  2014-06-12 02:39:02,915 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-cluster/00_base.yml
  2014-06-12 02:39:02,919 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-cluster/rhel-6-cluster-1/00_base.yml
  2014-06-12 02:39:02,921 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-cluster/rhel-6-cluster-2/00_base.yml
  2014-06-12 02:39:02,923 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-lvs-rs/00_base.yml
  2014-06-12 02:39:02,926 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-lvs-rs/rhel-6-lvs-rs-1/00_base.yml
  2014-06-12 02:39:02,928 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-lvs-rs/rhel-6-lvs-rs-2/00_base.yml
  2014-06-12 02:39:02,931 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-lvs/00_base.yml
  2014-06-12 02:39:02,936 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-lvs/rhel-6-lvs-1/00_base.yml
  2014-06-12 02:39:02,938 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-lvs/rhel-6-lvs-2/00_base.yml
  2014-06-12 02:39:02,942 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-proxy/00_base.yml
  2014-06-12 02:39:02,945 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhel-6-proxy/rhel-6-proxy-1/00_base.yml
  2014-06-12 02:39:02,947 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhevh/00_base.yml
  2014-06-12 02:39:02,949 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhevh/rhevh-2/00_base.yml
  2014-06-12 02:39:02,950 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhevm/00_base.yml
  2014-06-12 02:39:02,953 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhevm/rhevm-1/00_base.yml
  2014-06-12 02:39:02,955 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhs/00_base.yml
  2014-06-12 02:39:02,958 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhs/rhs-1/00_base.yml
  2014-06-12 02:39:02,960 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhs/rhs-2/00_base.yml
  2014-06-12 02:39:02,962 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhs/rhs-3/00_base.yml
  2014-06-12 02:39:02,964 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/rhs/rhs-4/00_base.yml
  2014-06-12 02:39:02,966 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/sam/00_base.yml
  2014-06-12 02:39:02,967 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/sam/sam-1/00_base.yml
  2014-06-12 02:39:02,968 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/satellite/00_base.yml
  2014-06-12 02:39:02,972 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/satellite/satellite-1/00_base.yml
  2014-06-12 02:39:02,973 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/satellite6/00_base.yml
  2014-06-12 02:39:02,977 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/satellite6/satellite6-1/00_base.yml
  2014-06-12 02:39:02,978 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/fedora/00_base.yml
  2014-06-12 02:39:02,979 anyconfig: [INFO] Dumping: /tmp/w/default/guests.d/fedora/fedora-20-1/00_base.yml
  2014-06-12 02:39:02,980 miniascape: [INFO] Loading host config files
  2014-06-12 02:39:02,980 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:02,997 anyconfig: [INFO] Loading: /tmp/w/default/host.d/00_base.yml
  2014-06-12 02:39:03,004 miniascape: [INFO] Loading guest config files: fedora-20-1
  2014-06-12 02:39:03,004 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,021 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/fedora/00_base.yml
  2014-06-12 02:39:03,022 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/fedora/fedora-20-1/00_base.yml
  2014-06-12 02:39:03,024 miniascape: [INFO] Loading guest config files: ipa-1
  2014-06-12 02:39:03,024 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,037 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/ipa/00_base.yml
  2014-06-12 02:39:03,040 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/ipa/ipa-1/00_base.yml
  2014-06-12 02:39:03,041 miniascape: [INFO] Loading guest config files: jboss-0
  2014-06-12 02:39:03,041 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,057 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/00_base.yml
  2014-06-12 02:39:03,063 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/jboss-0/00_base.yml
  2014-06-12 02:39:03,068 miniascape: [INFO] Loading guest config files: jboss-1
  2014-06-12 02:39:03,068 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,084 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/00_base.yml
  2014-06-12 02:39:03,089 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/jboss-1/00_base.yml
  2014-06-12 02:39:03,091 miniascape: [INFO] Loading guest config files: jboss-2
  2014-06-12 02:39:03,092 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,107 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/00_base.yml
  2014-06-12 02:39:03,113 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/jboss-2/00_base.yml
  2014-06-12 02:39:03,115 miniascape: [INFO] Loading guest config files: jboss-3
  2014-06-12 02:39:03,115 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,129 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/00_base.yml
  2014-06-12 02:39:03,136 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/jboss-3/00_base.yml
  2014-06-12 02:39:03,139 miniascape: [INFO] Loading guest config files: jboss-4
  2014-06-12 02:39:03,140 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,153 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/00_base.yml
  2014-06-12 02:39:03,160 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/jboss-4/00_base.yml
  2014-06-12 02:39:03,163 miniascape: [INFO] Loading guest config files: rhds-1
  2014-06-12 02:39:03,163 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,180 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhds/00_base.yml
  2014-06-12 02:39:03,183 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhds/rhds-1/00_base.yml
  2014-06-12 02:39:03,184 miniascape: [INFO] Loading guest config files: rhel-5-client-1
  2014-06-12 02:39:03,184 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,202 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-client/00_base.yml
  2014-06-12 02:39:03,205 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-client/rhel-5-client-1/00_base.yml
  2014-06-12 02:39:03,206 miniascape: [INFO] Loading guest config files: rhel-5-client-2
  2014-06-12 02:39:03,206 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,220 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-client/00_base.yml
  2014-06-12 02:39:03,223 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-client/rhel-5-client-2/00_base.yml
  2014-06-12 02:39:03,225 miniascape: [INFO] Loading guest config files: rhel-5-cluster-1
  2014-06-12 02:39:03,225 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,241 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-cluster/00_base.yml
  2014-06-12 02:39:03,249 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-cluster/rhel-5-cluster-1/00_base.yml
  2014-06-12 02:39:03,252 miniascape: [INFO] Loading guest config files: rhel-5-cluster-2
  2014-06-12 02:39:03,252 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,270 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-cluster/00_base.yml
  2014-06-12 02:39:03,277 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-cluster/rhel-5-cluster-2/00_base.yml
  2014-06-12 02:39:03,281 miniascape: [INFO] Loading guest config files: rhel-6-client-1
  2014-06-12 02:39:03,281 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,298 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-client/00_base.yml
  2014-06-12 02:39:03,299 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-client/rhel-6-client-1/00_base.yml
  2014-06-12 02:39:03,301 miniascape: [INFO] Loading guest config files: rhel-6-cluster-1
  2014-06-12 02:39:03,301 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,314 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster/00_base.yml
  2014-06-12 02:39:03,324 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster/rhel-6-cluster-1/00_base.yml
  2014-06-12 02:39:03,328 miniascape: [INFO] Loading guest config files: rhel-6-cluster-2
  2014-06-12 02:39:03,328 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,341 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster/00_base.yml
  2014-06-12 02:39:03,349 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster/rhel-6-cluster-2/00_base.yml
  2014-06-12 02:39:03,354 miniascape: [INFO] Loading guest config files: rhel-6-cluster-gfs-1
  2014-06-12 02:39:03,354 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,369 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster-gfs/00_base.yml
  2014-06-12 02:39:03,383 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster-gfs/rhel-6-cluster-gfs-1/00_base.yml
  2014-06-12 02:39:03,387 miniascape: [INFO] Loading guest config files: rhel-6-cluster-gfs-2
  2014-06-12 02:39:03,387 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,400 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster-gfs/00_base.yml
  2014-06-12 02:39:03,416 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster-gfs/rhel-6-cluster-gfs-2/00_base.yml
  2014-06-12 02:39:03,419 miniascape: [INFO] Loading guest config files: rhel-6-cluster-gfs-3
  2014-06-12 02:39:03,419 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,433 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster-gfs/00_base.yml
  2014-06-12 02:39:03,448 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster-gfs/rhel-6-cluster-gfs-3/00_base.yml
  2014-06-12 02:39:03,451 miniascape: [INFO] Loading guest config files: rhel-6-lvs-1
  2014-06-12 02:39:03,451 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,465 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs/00_base.yml
  2014-06-12 02:39:03,475 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs/rhel-6-lvs-1/00_base.yml
  2014-06-12 02:39:03,479 miniascape: [INFO] Loading guest config files: rhel-6-lvs-2
  2014-06-12 02:39:03,479 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,493 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs/00_base.yml
  2014-06-12 02:39:03,502 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs/rhel-6-lvs-2/00_base.yml
  2014-06-12 02:39:03,507 miniascape: [INFO] Loading guest config files: rhel-6-lvs-rs-1
  2014-06-12 02:39:03,507 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,521 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs-rs/00_base.yml
  2014-06-12 02:39:03,523 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs-rs/rhel-6-lvs-rs-1/00_base.yml
  2014-06-12 02:39:03,527 miniascape: [INFO] Loading guest config files: rhel-6-lvs-rs-2
  2014-06-12 02:39:03,527 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,545 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs-rs/00_base.yml
  2014-06-12 02:39:03,547 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs-rs/rhel-6-lvs-rs-2/00_base.yml
  2014-06-12 02:39:03,551 miniascape: [INFO] Loading guest config files: rhel-6-mrg-m-1
  2014-06-12 02:39:03,551 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,567 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-mrg-m/00_base.yml
  2014-06-12 02:39:03,571 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-mrg-m/rhel-6-mrg-m-1/00_base.yml
  2014-06-12 02:39:03,572 miniascape: [INFO] Loading guest config files: rhel-6-mrg-m-2
  2014-06-12 02:39:03,572 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,586 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-mrg-m/00_base.yml
  2014-06-12 02:39:03,589 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-mrg-m/rhel-6-mrg-m-2/00_base.yml
  2014-06-12 02:39:03,592 miniascape: [INFO] Loading guest config files: rhel-6-proxy-1
  2014-06-12 02:39:03,592 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,608 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-proxy/00_base.yml
  2014-06-12 02:39:03,611 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-proxy/rhel-6-proxy-1/00_base.yml
  2014-06-12 02:39:03,614 miniascape: [INFO] Loading guest config files: rhevh-2
  2014-06-12 02:39:03,615 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,632 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhevh/00_base.yml
  2014-06-12 02:39:03,635 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhevh/rhevh-2/00_base.yml
  2014-06-12 02:39:03,636 miniascape: [INFO] Loading guest config files: rhevm-1
  2014-06-12 02:39:03,636 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,650 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhevm/00_base.yml
  2014-06-12 02:39:03,657 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhevm/rhevm-1/00_base.yml
  2014-06-12 02:39:03,660 miniascape: [INFO] Loading guest config files: rhs-1
  2014-06-12 02:39:03,660 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,673 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/00_base.yml
  2014-06-12 02:39:03,677 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/rhs-1/00_base.yml
  2014-06-12 02:39:03,679 miniascape: [INFO] Loading guest config files: rhs-2
  2014-06-12 02:39:03,679 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,697 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/00_base.yml
  2014-06-12 02:39:03,700 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/rhs-2/00_base.yml
  2014-06-12 02:39:03,703 miniascape: [INFO] Loading guest config files: rhs-3
  2014-06-12 02:39:03,703 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,720 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/00_base.yml
  2014-06-12 02:39:03,723 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/rhs-3/00_base.yml
  2014-06-12 02:39:03,726 miniascape: [INFO] Loading guest config files: rhs-4
  2014-06-12 02:39:03,726 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,740 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/00_base.yml
  2014-06-12 02:39:03,743 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/rhs-4/00_base.yml
  2014-06-12 02:39:03,748 miniascape: [INFO] Loading guest config files: sam-1
  2014-06-12 02:39:03,748 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,762 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/sam/00_base.yml
  2014-06-12 02:39:03,764 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/sam/sam-1/00_base.yml
  2014-06-12 02:39:03,766 miniascape: [INFO] Loading guest config files: satellite-1
  2014-06-12 02:39:03,766 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,783 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/satellite/00_base.yml
  2014-06-12 02:39:03,789 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/satellite/satellite-1/00_base.yml
  2014-06-12 02:39:03,791 miniascape: [INFO] Loading guest config files: satellite6-1
  2014-06-12 02:39:03,791 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,805 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/satellite6/00_base.yml
  2014-06-12 02:39:03,815 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/satellite6/satellite6-1/00_base.yml
  2014-06-12 02:39:03,816 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,830 anyconfig: [INFO] Loading: /tmp/w/default/networks.d/default/00_base.yml
  2014-06-12 02:39:03,833 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:03,849 anyconfig: [INFO] Loading: /tmp/w/default/networks.d/service/00_base.yml
  2014-06-12 02:39:03,852 anyconfig: [INFO] Dumping: /tmp/w/host/usr/share/miniascape/networks.d/default.yml
  2014-06-12 02:39:03,874 anyconfig: [INFO] Loading: /tmp/w/host/usr/share/miniascape/networks.d/default.yml
  2014-06-12 02:39:03,923 anyconfig: [INFO] Dumping: /tmp/w/host/usr/share/miniascape/networks.d/service.yml
  2014-06-12 02:39:03,958 anyconfig: [INFO] Loading: /tmp/w/host/usr/share/miniascape/networks.d/service.yml
  2014-06-12 02:39:04,030 miniascape: [INFO] Generating /tmp/w/host/etc/httpd/conf.d/miniascape_autoinst.conf from miniascape_autoinst.conf [apache_autoinst_conf]
  2014-06-12 02:39:04,032 miniascape: [INFO] Generating /tmp/w/host/usr/libexec/miniascape/guest_network_register.sh from guest_network_register.sh [register_guest_dns_and_dhcp_entry_to_virt_network]
  2014-06-12 02:39:04,035 miniascape: [INFO] Generating /tmp/w/host/usr/libexec/miniascape/default/create_lio_iscsi_lun.sh from create_lio_iscsi_lun.sh [create_lio_iscsi_lun]
  2014-06-12 02:39:04,040 miniascape: [INFO] Generating /tmp/w/host/rpm.mk from rpm.mk [rpm_mk]
  2014-06-12 02:39:04,041 miniascape: [INFO] Generating /tmp/w/host/usr/libexec/miniascape/register_libvirt_network.sh from register_libvirt_network.sh [register_libvirt_network]
  2014-06-12 02:39:04,043 miniascape: [INFO] Generating /tmp/w/host/Makefile.am from Makefile.am [Makefile_am]
  2014-06-12 02:39:04,044 miniascape: [INFO] Generating /tmp/w/host/etc/modprobe.d/kvm.conf from kvm.conf [enable_nested_kvm]
  2014-06-12 02:39:04,045 miniascape: [INFO] Generating /tmp/w/host/package.spec from package.spec [rpm_spec]
  2014-06-12 02:39:04,049 miniascape: [INFO] Generating /tmp/w/host/etc/auto.master.d/isos.autofs from isos.autofs [auto_isos_master]
  2014-06-12 02:39:04,050 miniascape: [INFO] Generating /tmp/w/host/etc/auto.isos from auto.isos [auto_isos_map]
  2014-06-12 02:39:04,053 miniascape: [INFO] Generating /tmp/w/host/etc/fence_virt.conf from fence_virt.conf [fence_virt]
  2014-06-12 02:39:04,055 miniascape: [INFO] Generating /tmp/w/host/usr/libexec/miniascape/default/fixup_software_bridge.sh from fixup_software_bridge.sh [fixup_software_bridge]
  2014-06-12 02:39:04,056 miniascape: [INFO] Generating /tmp/w/host/configure.ac from configure.ac [configure_ac]
  2014-06-12 02:39:04,059 miniascape: [INFO] Loading guest config files: fedora-20-1
  2014-06-12 02:39:04,059 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:04,078 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/fedora/00_base.yml
  2014-06-12 02:39:04,079 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/fedora/fedora-20-1/00_base.yml
  2014-06-12 02:39:04,080 miniascape: [INFO] Generating setup data archive to embedded: fedora-20-1
  2014-06-12 02:39:04,080 miniascape: [INFO] Generating /tmp/w/guests.d/fedora-20-1/ks.cfg from fedora-min-ks.cfg [autoinst]
  2014-06-12 02:39:04,139 miniascape: [INFO] Generating /tmp/w/guests.d/fedora-20-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:04,141 miniascape: [INFO] Generating /tmp/w/guests.d/fedora-20-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:04,145 miniascape: [INFO] Generating /tmp/w/guests.d/fedora-20-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:04,181 miniascape: [INFO] Loading guest config files: ipa-1
  2014-06-12 02:39:04,181 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:04,194 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/ipa/00_base.yml
  2014-06-12 02:39:04,197 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/ipa/ipa-1/00_base.yml
  2014-06-12 02:39:04,198 miniascape: [INFO] Generating setup data archive to embedded: ipa-1
  2014-06-12 02:39:04,198 miniascape: [INFO] Generating /tmp/w/guests.d/ipa-1/setup/setup.sh from data/ipa/setup.sh
  2014-06-12 02:39:04,217 miniascape: [INFO] Generating /tmp/w/guests.d/ipa-1/ks.cfg from ipa-ks.cfg [autoinst]
  2014-06-12 02:39:04,315 miniascape: [INFO] Generating /tmp/w/guests.d/ipa-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:04,317 miniascape: [INFO] Generating /tmp/w/guests.d/ipa-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:04,321 miniascape: [INFO] Generating /tmp/w/guests.d/ipa-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:04,357 miniascape: [INFO] Loading guest config files: jboss-0
  2014-06-12 02:39:04,358 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:04,371 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/00_base.yml
  2014-06-12 02:39:04,377 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/jboss-0/00_base.yml
  2014-06-12 02:39:04,382 miniascape: [INFO] Generating setup data archive to embedded: jboss-0
  2014-06-12 02:39:04,382 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-0/setup/Makefile from data/jboss/Makefile
  2014-06-12 02:39:04,389 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-0/setup/domain-0.xml from data/jboss/domain-0.xml
  2014-06-12 02:39:04,427 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-0/setup/host-master-0.xml from data/jboss/host-master-0.xml
  2014-06-12 02:39:04,429 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-0/setup/domain-app-deploy.sh from data/jboss/domain-app-deploy.sh
  2014-06-12 02:39:04,481 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-0/ks.cfg from rhel-6-jboss-ks.cfg [autoinst]
  2014-06-12 02:39:04,605 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-0/Makefile from Makefile [Makefile]
  2014-06-12 02:39:04,607 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-0/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:04,611 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-0/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:04,648 miniascape: [INFO] Loading guest config files: jboss-1
  2014-06-12 02:39:04,648 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:04,662 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/00_base.yml
  2014-06-12 02:39:04,667 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/jboss-1/00_base.yml
  2014-06-12 02:39:04,669 miniascape: [INFO] Generating setup data archive to embedded: jboss-1
  2014-06-12 02:39:04,669 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-1/setup/Makefile from data/jboss/Makefile
  2014-06-12 02:39:04,676 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-1/setup/host-slave-0.xml from data/jboss/host-slave-0.xml
  2014-06-12 02:39:04,704 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-1/ks.cfg from rhel-6-jboss-ks.cfg [autoinst]
  2014-06-12 02:39:04,797 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:04,799 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:04,803 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:04,840 miniascape: [INFO] Loading guest config files: jboss-2
  2014-06-12 02:39:04,840 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:04,858 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/00_base.yml
  2014-06-12 02:39:04,864 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/jboss-2/00_base.yml
  2014-06-12 02:39:04,867 miniascape: [INFO] Generating setup data archive to embedded: jboss-2
  2014-06-12 02:39:04,868 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-2/setup/Makefile from data/jboss/Makefile
  2014-06-12 02:39:04,873 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-2/setup/host-slave-0.xml from data/jboss/host-slave-0.xml
  2014-06-12 02:39:04,906 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-2/ks.cfg from rhel-6-jboss-ks.cfg [autoinst]
  2014-06-12 02:39:05,004 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-2/Makefile from Makefile [Makefile]
  2014-06-12 02:39:05,006 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-2/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:05,010 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-2/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:05,044 miniascape: [INFO] Loading guest config files: jboss-3
  2014-06-12 02:39:05,044 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:05,058 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/00_base.yml
  2014-06-12 02:39:05,063 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/jboss-3/00_base.yml
  2014-06-12 02:39:05,065 miniascape: [INFO] Generating setup data archive to embedded: jboss-3
  2014-06-12 02:39:05,066 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-3/setup/Makefile from data/jboss/Makefile
  2014-06-12 02:39:05,071 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-3/setup/host-slave-0.xml from data/jboss/host-slave-0.xml
  2014-06-12 02:39:05,102 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-3/ks.cfg from rhel-6-jboss-ks.cfg [autoinst]
  2014-06-12 02:39:05,199 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-3/Makefile from Makefile [Makefile]
  2014-06-12 02:39:05,200 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-3/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:05,205 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-3/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:05,238 miniascape: [INFO] Loading guest config files: jboss-4
  2014-06-12 02:39:05,238 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:05,252 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/00_base.yml
  2014-06-12 02:39:05,257 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/jboss/jboss-4/00_base.yml
  2014-06-12 02:39:05,259 miniascape: [INFO] Generating setup data archive to embedded: jboss-4
  2014-06-12 02:39:05,259 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-4/setup/Makefile from data/jboss/Makefile
  2014-06-12 02:39:05,264 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-4/setup/host-slave-0.xml from data/jboss/host-slave-0.xml
  2014-06-12 02:39:05,291 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-4/ks.cfg from rhel-6-jboss-ks.cfg [autoinst]
  2014-06-12 02:39:05,389 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-4/Makefile from Makefile [Makefile]
  2014-06-12 02:39:05,391 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-4/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:05,395 miniascape: [INFO] Generating /tmp/w/guests.d/jboss-4/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:05,429 miniascape: [INFO] Loading guest config files: rhds-1
  2014-06-12 02:39:05,429 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:05,442 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhds/00_base.yml
  2014-06-12 02:39:05,445 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhds/rhds-1/00_base.yml
  2014-06-12 02:39:05,446 miniascape: [INFO] Generating setup data archive to embedded: rhds-1
  2014-06-12 02:39:05,447 miniascape: [INFO] Generating /tmp/w/guests.d/rhds-1/setup/setup.inf from data/rhds/setup.inf
  2014-06-12 02:39:05,448 miniascape: [INFO] Generating /tmp/w/guests.d/rhds-1/setup/Makefile from data/rhds/Makefile
  2014-06-12 02:39:05,481 miniascape: [INFO] Generating /tmp/w/guests.d/rhds-1/ks.cfg from rhds-ks.cfg [autoinst]
  2014-06-12 02:39:05,581 miniascape: [INFO] Generating /tmp/w/guests.d/rhds-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:05,583 miniascape: [INFO] Generating /tmp/w/guests.d/rhds-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:05,587 miniascape: [INFO] Generating /tmp/w/guests.d/rhds-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:05,621 miniascape: [INFO] Loading guest config files: rhel-5-client-1
  2014-06-12 02:39:05,621 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:05,636 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-client/00_base.yml
  2014-06-12 02:39:05,639 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-client/rhel-5-client-1/00_base.yml
  2014-06-12 02:39:05,640 miniascape: [INFO] Generating setup data archive to embedded: rhel-5-client-1
  2014-06-12 02:39:05,640 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-client-1/ks.cfg from rhel-5-min-ks.cfg [autoinst]
  2014-06-12 02:39:05,715 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-client-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:05,717 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-client-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:05,721 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-client-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:05,755 miniascape: [INFO] Loading guest config files: rhel-5-client-2
  2014-06-12 02:39:05,755 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:05,769 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-client/00_base.yml
  2014-06-12 02:39:05,772 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-client/rhel-5-client-2/00_base.yml
  2014-06-12 02:39:05,773 miniascape: [INFO] Generating setup data archive to embedded: rhel-5-client-2
  2014-06-12 02:39:05,774 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-client-2/ks.cfg from rhel-5-min-ks.cfg [autoinst]
  2014-06-12 02:39:05,853 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-client-2/Makefile from Makefile [Makefile]
  2014-06-12 02:39:05,855 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-client-2/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:05,859 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-client-2/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:05,893 miniascape: [INFO] Loading guest config files: rhel-5-cluster-1
  2014-06-12 02:39:05,893 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:05,906 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-cluster/00_base.yml
  2014-06-12 02:39:05,914 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-cluster/rhel-5-cluster-1/00_base.yml
  2014-06-12 02:39:05,917 miniascape: [INFO] Generating setup data archive to embedded: rhel-5-cluster-1
  2014-06-12 02:39:05,917 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-cluster-1/setup/cluster.conf from data/rhel-5-cluster/cluster.conf
  2014-06-12 02:39:05,922 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-cluster-1/setup/init_qdisk.sh from data/rhel-5-cluster/init_qdisk.sh
  2014-06-12 02:39:05,964 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-cluster-1/ks.cfg from rhel-5-cluster-ks.cfg [autoinst]
  2014-06-12 02:39:06,064 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-cluster-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:06,066 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-cluster-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:06,070 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-cluster-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:06,104 miniascape: [INFO] Loading guest config files: rhel-5-cluster-2
  2014-06-12 02:39:06,104 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:06,118 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-cluster/00_base.yml
  2014-06-12 02:39:06,126 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-5-cluster/rhel-5-cluster-2/00_base.yml
  2014-06-12 02:39:06,129 miniascape: [INFO] Generating setup data archive to embedded: rhel-5-cluster-2
  2014-06-12 02:39:06,129 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-cluster-2/setup/cluster.conf from data/rhel-5-cluster/cluster.conf
  2014-06-12 02:39:06,134 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-cluster-2/setup/init_qdisk.sh from data/rhel-5-cluster/init_qdisk.sh
  2014-06-12 02:39:06,165 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-cluster-2/ks.cfg from rhel-5-cluster-ks.cfg [autoinst]
  2014-06-12 02:39:06,265 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-cluster-2/Makefile from Makefile [Makefile]
  2014-06-12 02:39:06,267 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-cluster-2/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:06,271 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-5-cluster-2/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:06,304 miniascape: [INFO] Loading guest config files: rhel-6-client-1
  2014-06-12 02:39:06,305 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:06,319 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-client/00_base.yml
  2014-06-12 02:39:06,321 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-client/rhel-6-client-1/00_base.yml
  2014-06-12 02:39:06,322 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-client-1
  2014-06-12 02:39:06,322 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-client-1/ks.cfg from rhel-6-min-ks.cfg [autoinst]
  2014-06-12 02:39:06,402 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-client-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:06,404 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-client-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:06,408 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-client-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:06,442 miniascape: [INFO] Loading guest config files: rhel-6-cluster-1
  2014-06-12 02:39:06,442 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:06,456 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster/00_base.yml
  2014-06-12 02:39:06,463 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster/rhel-6-cluster-1/00_base.yml
  2014-06-12 02:39:06,466 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-cluster-1
  2014-06-12 02:39:06,466 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-1/setup/cluster.conf from data/rhel-5-cluster/cluster.conf
  2014-06-12 02:39:06,471 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-1/setup/init_qdisk.sh from data/rhel-5-cluster/init_qdisk.sh
  2014-06-12 02:39:06,513 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-1/ks.cfg from rhel-6-cluster-ks.cfg [autoinst]
  2014-06-12 02:39:06,619 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:06,621 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:06,626 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:06,659 miniascape: [INFO] Loading guest config files: rhel-6-cluster-2
  2014-06-12 02:39:06,660 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:06,674 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster/00_base.yml
  2014-06-12 02:39:06,680 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster/rhel-6-cluster-2/00_base.yml
  2014-06-12 02:39:06,683 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-cluster-2
  2014-06-12 02:39:06,684 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-2/setup/cluster.conf from data/rhel-5-cluster/cluster.conf
  2014-06-12 02:39:06,688 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-2/setup/init_qdisk.sh from data/rhel-5-cluster/init_qdisk.sh
  2014-06-12 02:39:06,732 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-2/ks.cfg from rhel-6-cluster-ks.cfg [autoinst]
  2014-06-12 02:39:06,848 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-2/Makefile from Makefile [Makefile]
  2014-06-12 02:39:06,850 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-2/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:06,854 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-2/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:06,888 miniascape: [INFO] Loading guest config files: rhel-6-cluster-gfs-1
  2014-06-12 02:39:06,888 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:06,902 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster-gfs/00_base.yml
  2014-06-12 02:39:06,913 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster-gfs/rhel-6-cluster-gfs-1/00_base.yml
  2014-06-12 02:39:06,917 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-cluster-gfs-1
  2014-06-12 02:39:06,917 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-1/setup/cluster.conf from data/rhel-6-cluster-gfs/cluster.conf
  2014-06-12 02:39:06,922 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-1/setup/init_gfs.sh from data/rhel-6-cluster-gfs/init_gfs.sh
  2014-06-12 02:39:06,938 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-1/setup/check_cman.sh from data/rhel-6-cluster-gfs/check_cman.sh
  2014-06-12 02:39:06,939 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-1/setup/start_cman.sh from data/rhel-6-cluster-gfs/start_cman.sh
  2014-06-12 02:39:06,940 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-1/setup/start_clvmd.sh from data/rhel-6-cluster-gfs/start_clvmd.sh
  2014-06-12 02:39:06,960 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-1/ks.cfg from rhel-6-cluster-gfs-ks.cfg [autoinst]
  2014-06-12 02:39:07,082 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:07,084 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:07,088 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:07,123 miniascape: [INFO] Loading guest config files: rhel-6-cluster-gfs-2
  2014-06-12 02:39:07,123 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:07,137 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster-gfs/00_base.yml
  2014-06-12 02:39:07,149 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster-gfs/rhel-6-cluster-gfs-2/00_base.yml
  2014-06-12 02:39:07,153 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-cluster-gfs-2
  2014-06-12 02:39:07,153 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-2/setup/cluster.conf from data/rhel-6-cluster-gfs/cluster.conf
  2014-06-12 02:39:07,158 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-2/setup/init_gfs.sh from data/rhel-6-cluster-gfs/init_gfs.sh
  2014-06-12 02:39:07,173 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-2/setup/check_cman.sh from data/rhel-6-cluster-gfs/check_cman.sh
  2014-06-12 02:39:07,174 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-2/setup/start_cman.sh from data/rhel-6-cluster-gfs/start_cman.sh
  2014-06-12 02:39:07,175 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-2/setup/start_clvmd.sh from data/rhel-6-cluster-gfs/start_clvmd.sh
  2014-06-12 02:39:07,191 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-2/ks.cfg from rhel-6-cluster-gfs-ks.cfg [autoinst]
  2014-06-12 02:39:07,303 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-2/Makefile from Makefile [Makefile]
  2014-06-12 02:39:07,305 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-2/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:07,309 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-2/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:07,347 miniascape: [INFO] Loading guest config files: rhel-6-cluster-gfs-3
  2014-06-12 02:39:07,347 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:07,360 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster-gfs/00_base.yml
  2014-06-12 02:39:07,375 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-cluster-gfs/rhel-6-cluster-gfs-3/00_base.yml
  2014-06-12 02:39:07,379 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-cluster-gfs-3
  2014-06-12 02:39:07,379 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-3/setup/cluster.conf from data/rhel-6-cluster-gfs/cluster.conf
  2014-06-12 02:39:07,384 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-3/setup/init_gfs.sh from data/rhel-6-cluster-gfs/init_gfs.sh
  2014-06-12 02:39:07,399 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-3/setup/check_cman.sh from data/rhel-6-cluster-gfs/check_cman.sh
  2014-06-12 02:39:07,401 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-3/setup/start_cman.sh from data/rhel-6-cluster-gfs/start_cman.sh
  2014-06-12 02:39:07,402 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-3/setup/start_clvmd.sh from data/rhel-6-cluster-gfs/start_clvmd.sh
  2014-06-12 02:39:07,422 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-3/ks.cfg from rhel-6-cluster-gfs-ks.cfg [autoinst]
  2014-06-12 02:39:07,546 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-3/Makefile from Makefile [Makefile]
  2014-06-12 02:39:07,548 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-3/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:07,552 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-cluster-gfs-3/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:07,588 miniascape: [INFO] Loading guest config files: rhel-6-lvs-1
  2014-06-12 02:39:07,589 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:07,602 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs/00_base.yml
  2014-06-12 02:39:07,610 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs/rhel-6-lvs-1/00_base.yml
  2014-06-12 02:39:07,616 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-lvs-1
  2014-06-12 02:39:07,616 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-1/setup/Makefile from data/lvs/Makefile
  2014-06-12 02:39:07,617 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-1/setup/setup_nat.sh from data/lvs/setup_nat.sh
  2014-06-12 02:39:07,622 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-1/setup/setup_dr.sh from data/lvs/setup_dr.sh
  2014-06-12 02:39:07,656 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-1/ks.cfg from rhel-6-lvs-ks.cfg [autoinst]
  2014-06-12 02:39:07,762 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:07,764 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:07,768 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:07,805 miniascape: [INFO] Loading guest config files: rhel-6-lvs-2
  2014-06-12 02:39:07,805 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:07,819 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs/00_base.yml
  2014-06-12 02:39:07,827 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs/rhel-6-lvs-2/00_base.yml
  2014-06-12 02:39:07,833 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-lvs-2
  2014-06-12 02:39:07,833 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-2/setup/Makefile from data/lvs/Makefile
  2014-06-12 02:39:07,834 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-2/setup/setup_nat.sh from data/lvs/setup_nat.sh
  2014-06-12 02:39:07,838 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-2/setup/setup_dr.sh from data/lvs/setup_dr.sh
  2014-06-12 02:39:07,875 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-2/ks.cfg from rhel-6-lvs-ks.cfg [autoinst]
  2014-06-12 02:39:07,992 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-2/Makefile from Makefile [Makefile]
  2014-06-12 02:39:07,994 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-2/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:07,998 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-2/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:08,035 miniascape: [INFO] Loading guest config files: rhel-6-lvs-rs-1
  2014-06-12 02:39:08,035 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:08,049 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs-rs/00_base.yml
  2014-06-12 02:39:08,051 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs-rs/rhel-6-lvs-rs-1/00_base.yml
  2014-06-12 02:39:08,055 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-lvs-rs-1
  2014-06-12 02:39:08,055 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-rs-1/setup/setup_dr.sh from data/lvs-rs/setup_dr.sh
  2014-06-12 02:39:08,077 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-rs-1/ks.cfg from rhel-6-lvs-rs-ks.cfg [autoinst]
  2014-06-12 02:39:08,168 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-rs-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:08,170 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-rs-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:08,174 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-rs-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:08,208 miniascape: [INFO] Loading guest config files: rhel-6-lvs-rs-2
  2014-06-12 02:39:08,208 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:08,222 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs-rs/00_base.yml
  2014-06-12 02:39:08,225 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-lvs-rs/rhel-6-lvs-rs-2/00_base.yml
  2014-06-12 02:39:08,229 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-lvs-rs-2
  2014-06-12 02:39:08,229 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-rs-2/setup/setup_dr.sh from data/lvs-rs/setup_dr.sh
  2014-06-12 02:39:08,258 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-rs-2/ks.cfg from rhel-6-lvs-rs-ks.cfg [autoinst]
  2014-06-12 02:39:08,352 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-rs-2/Makefile from Makefile [Makefile]
  2014-06-12 02:39:08,354 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-rs-2/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:08,358 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-lvs-rs-2/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:08,392 miniascape: [INFO] Loading guest config files: rhel-6-mrg-m-1
  2014-06-12 02:39:08,392 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:08,406 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-mrg-m/00_base.yml
  2014-06-12 02:39:08,410 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-mrg-m/rhel-6-mrg-m-1/00_base.yml
  2014-06-12 02:39:08,412 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-mrg-m-1
  2014-06-12 02:39:08,412 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-mrg-m-1/setup/qpidd_cluster_check.py from data/mrg-m/qpidd_cluster_check.py.txt
  2014-06-12 02:39:08,441 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-mrg-m-1/ks.cfg from rhel-6-mrg-m-ks.cfg [autoinst]
  2014-06-12 02:39:08,536 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-mrg-m-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:08,538 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-mrg-m-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:08,542 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-mrg-m-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:08,578 miniascape: [INFO] Loading guest config files: rhel-6-mrg-m-2
  2014-06-12 02:39:08,579 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:08,593 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-mrg-m/00_base.yml
  2014-06-12 02:39:08,597 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-mrg-m/rhel-6-mrg-m-2/00_base.yml
  2014-06-12 02:39:08,598 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-mrg-m-2
  2014-06-12 02:39:08,598 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-mrg-m-2/setup/qpidd_cluster_check.py from data/mrg-m/qpidd_cluster_check.py.txt
  2014-06-12 02:39:08,627 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-mrg-m-2/ks.cfg from rhel-6-mrg-m-ks.cfg [autoinst]
  2014-06-12 02:39:08,711 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-mrg-m-2/Makefile from Makefile [Makefile]
  2014-06-12 02:39:08,713 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-mrg-m-2/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:08,717 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-mrg-m-2/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:08,751 miniascape: [INFO] Loading guest config files: rhel-6-proxy-1
  2014-06-12 02:39:08,752 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:08,766 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-proxy/00_base.yml
  2014-06-12 02:39:08,768 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhel-6-proxy/rhel-6-proxy-1/00_base.yml
  2014-06-12 02:39:08,772 miniascape: [INFO] Generating setup data archive to embedded: rhel-6-proxy-1
  2014-06-12 02:39:08,772 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-proxy-1/setup/squid.conf from data/proxy/squid.conf
  2014-06-12 02:39:08,799 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-proxy-1/ks.cfg from rhel-6-proxy-ks.cfg [autoinst]
  2014-06-12 02:39:08,906 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-proxy-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:08,908 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-proxy-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:08,912 miniascape: [INFO] Generating /tmp/w/guests.d/rhel-6-proxy-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:08,947 miniascape: [INFO] Loading guest config files: rhevh-2
  2014-06-12 02:39:08,947 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:08,961 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhevh/00_base.yml
  2014-06-12 02:39:08,964 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhevh/rhevh-2/00_base.yml
  2014-06-12 02:39:08,966 miniascape: [INFO] Generating setup data archive to embedded: rhevh-2
  2014-06-12 02:39:08,966 miniascape: [WARNING] autoinst lacks 'src' parameter
  2014-06-12 02:39:08,966 miniascape: [WARNING] autoinst lacks 'src' parameter
  2014-06-12 02:39:08,966 miniascape: [INFO] Generating /tmp/w/guests.d/rhevh-2/Makefile from Makefile [Makefile]
  2014-06-12 02:39:08,968 miniascape: [INFO] Generating /tmp/w/guests.d/rhevh-2/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:08,973 miniascape: [INFO] Generating /tmp/w/guests.d/rhevh-2/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:09,011 miniascape: [INFO] Loading guest config files: rhevm-1
  2014-06-12 02:39:09,011 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:09,027 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhevm/00_base.yml
  2014-06-12 02:39:09,032 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhevm/rhevm-1/00_base.yml
  2014-06-12 02:39:09,034 miniascape: [INFO] Generating setup data archive to embedded: rhevm-1
  2014-06-12 02:39:09,034 miniascape: [INFO] Generating /tmp/w/guests.d/rhevm-1/setup/Makefile from data/rhev-manager/Makefile
  2014-06-12 02:39:09,038 miniascape: [INFO] Generating /tmp/w/guests.d/rhevm-1/setup/answers.txt.last_half from data/rhev-manager/answers.txt
  2014-06-12 02:39:09,053 miniascape: [INFO] Generating /tmp/w/guests.d/rhevm-1/setup/rhevm_setup_wrapper.py from data/rhev-manager/rhevm_setup_wrapper.py.txt
  2014-06-12 02:39:09,076 miniascape: [INFO] Generating /tmp/w/guests.d/rhevm-1/ks.cfg from rhev-manager-ks.cfg [autoinst]
  2014-06-12 02:39:09,172 miniascape: [INFO] Generating /tmp/w/guests.d/rhevm-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:09,173 miniascape: [INFO] Generating /tmp/w/guests.d/rhevm-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:09,178 miniascape: [INFO] Generating /tmp/w/guests.d/rhevm-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:09,212 miniascape: [INFO] Loading guest config files: rhs-1
  2014-06-12 02:39:09,212 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:09,226 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/00_base.yml
  2014-06-12 02:39:09,229 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/rhs-1/00_base.yml
  2014-06-12 02:39:09,231 miniascape: [INFO] Generating setup data archive to embedded: rhs-1
  2014-06-12 02:39:09,231 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-1/ks.cfg from glusterfs-ks.cfg [autoinst]
  2014-06-12 02:39:09,319 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:09,320 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:09,325 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:09,359 miniascape: [INFO] Loading guest config files: rhs-2
  2014-06-12 02:39:09,359 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:09,373 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/00_base.yml
  2014-06-12 02:39:09,376 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/rhs-2/00_base.yml
  2014-06-12 02:39:09,378 miniascape: [INFO] Generating setup data archive to embedded: rhs-2
  2014-06-12 02:39:09,379 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-2/ks.cfg from glusterfs-ks.cfg [autoinst]
  2014-06-12 02:39:09,465 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-2/Makefile from Makefile [Makefile]
  2014-06-12 02:39:09,467 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-2/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:09,471 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-2/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:09,505 miniascape: [INFO] Loading guest config files: rhs-3
  2014-06-12 02:39:09,506 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:09,519 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/00_base.yml
  2014-06-12 02:39:09,522 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/rhs-3/00_base.yml
  2014-06-12 02:39:09,525 miniascape: [INFO] Generating setup data archive to embedded: rhs-3
  2014-06-12 02:39:09,525 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-3/ks.cfg from glusterfs-ks.cfg [autoinst]
  2014-06-12 02:39:09,614 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-3/Makefile from Makefile [Makefile]
  2014-06-12 02:39:09,616 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-3/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:09,620 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-3/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:09,654 miniascape: [INFO] Loading guest config files: rhs-4
  2014-06-12 02:39:09,654 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:09,668 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/00_base.yml
  2014-06-12 02:39:09,671 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/rhs/rhs-4/00_base.yml
  2014-06-12 02:39:09,674 miniascape: [INFO] Generating setup data archive to embedded: rhs-4
  2014-06-12 02:39:09,674 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-4/ks.cfg from glusterfs-ks.cfg [autoinst]
  2014-06-12 02:39:09,761 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-4/Makefile from Makefile [Makefile]
  2014-06-12 02:39:09,763 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-4/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:09,767 miniascape: [INFO] Generating /tmp/w/guests.d/rhs-4/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:09,801 miniascape: [INFO] Loading guest config files: sam-1
  2014-06-12 02:39:09,801 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:09,815 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/sam/00_base.yml
  2014-06-12 02:39:09,817 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/sam/sam-1/00_base.yml
  2014-06-12 02:39:09,818 miniascape: [INFO] Generating setup data archive to embedded: sam-1
  2014-06-12 02:39:09,818 miniascape: [INFO] Generating /tmp/w/guests.d/sam-1/ks.cfg from sam-ks.cfg [autoinst]
  2014-06-12 02:39:09,901 miniascape: [INFO] Generating /tmp/w/guests.d/sam-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:09,902 miniascape: [INFO] Generating /tmp/w/guests.d/sam-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:09,907 miniascape: [INFO] Generating /tmp/w/guests.d/sam-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:09,940 miniascape: [INFO] Loading guest config files: satellite-1
  2014-06-12 02:39:09,941 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:09,955 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/satellite/00_base.yml
  2014-06-12 02:39:09,961 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/satellite/satellite-1/00_base.yml
  2014-06-12 02:39:09,962 miniascape: [INFO] Generating setup data archive to embedded: satellite-1
  2014-06-12 02:39:09,962 miniascape: [INFO] Generating /tmp/w/guests.d/satellite-1/setup/Makefile from data/satellite/Makefile
  2014-06-12 02:39:09,963 miniascape: [INFO] Generating /tmp/w/guests.d/satellite-1/setup/answers.txt from data/satellite/answers.txt
  2014-06-12 02:39:09,971 miniascape: [INFO] Generating /tmp/w/guests.d/satellite-1/setup/switch-to-online-mode.sh from data/satellite/switch-to-online-mode.sh
  2014-06-12 02:39:09,988 miniascape: [INFO] Generating /tmp/w/guests.d/satellite-1/ks.cfg from satellite-ks.cfg [autoinst]
  2014-06-12 02:39:10,100 miniascape: [INFO] Generating /tmp/w/guests.d/satellite-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:10,101 miniascape: [INFO] Generating /tmp/w/guests.d/satellite-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:10,106 miniascape: [INFO] Generating /tmp/w/guests.d/satellite-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:10,142 miniascape: [INFO] Loading guest config files: satellite6-1
  2014-06-12 02:39:10,142 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:10,156 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/satellite6/00_base.yml
  2014-06-12 02:39:10,163 anyconfig: [INFO] Loading: /tmp/w/default/guests.d/satellite6/satellite6-1/00_base.yml
  2014-06-12 02:39:10,164 miniascape: [INFO] Generating setup data archive to embedded: satellite6-1
  2014-06-12 02:39:10,164 miniascape: [INFO] Generating /tmp/w/guests.d/satellite6-1/setup/Makefile from data/satellite6/Makefile
  2014-06-12 02:39:10,167 miniascape: [INFO] Generating /tmp/w/guests.d/satellite6-1/setup/answers.txt from data/satellite6/answers.txt
  2014-06-12 02:39:10,198 miniascape: [INFO] Generating /tmp/w/guests.d/satellite6-1/ks.cfg from satellite6-ks.cfg [autoinst]
  2014-06-12 02:39:10,294 miniascape: [INFO] Generating /tmp/w/guests.d/satellite6-1/Makefile from Makefile [Makefile]
  2014-06-12 02:39:10,296 miniascape: [INFO] Generating /tmp/w/guests.d/satellite6-1/net_register.sh from net_register.sh [netregist]
  2014-06-12 02:39:10,300 miniascape: [INFO] Generating /tmp/w/guests.d/satellite6-1/vmbuild.sh from vmbuild.sh [virtinst]
  2014-06-12 02:39:10,333 miniascape: [INFO] Loading host config files
  2014-06-12 02:39:10,333 anyconfig: [INFO] Loading: /tmp/w/default/common/00_base.yml
  2014-06-12 02:39:10,347 anyconfig: [INFO] Loading: /tmp/w/default/host.d/00_base.yml
  2014-06-12 02:39:10,354 miniascape: [INFO] Generating guests common build aux files...
  2014-06-12 02:39:10,354 miniascape: [INFO] Generating /tmp/w/guests.d/rpm.mk from rpm.mk [rpmmk]
  2014-06-12 02:39:10,355 miniascape: [INFO] Generating /tmp/w/guests.d/package.spec from package.spec [rpmspec]
  2014-06-12 02:39:10,359 miniascape: [INFO] Generating /tmp/w/guests.d/Makefile.am from Makefile.am [Makefile_am]
  2014-06-12 02:39:10,361 miniascape: [INFO] Generating /tmp/w/guests.d/configure.ac from configure.ac [configure_ac]
  ssato@localhost% ls /tmp/w                       ~/repos/public/github.com/ssato/miniascape.git
  default  guests.d  host
  ssato@localhost% ls /tmp/w/default/              ~/repos/public/github.com/ssato/miniascape.git
  common  guests.d  host.d  networks.d
  ssato@localhost% ls /tmp/w/default//*            ~/repos/public/github.com/ssato/miniascape.git
  /tmp/w/default//common:
  00_base.yml

  /tmp/w/default//guests.d:
  fedora  rhds            rhel-6-client       rhel-6-lvs     rhel-6-proxy  rhs        satellite6
  ipa     rhel-5-client   rhel-6-cluster      rhel-6-lvs-rs  rhevh         sam
  jboss   rhel-5-cluster  rhel-6-cluster-gfs  rhel-6-mrg-m   rhevm         satellite

  /tmp/w/default//host.d:
  00_base.yml

  /tmp/w/default//networks.d:
  default  service
  ssato@localhost% ls /tmp/w/guests.d              ~/repos/public/github.com/ssato/miniascape.git
  Makefile.am   jboss-3           rhel-5-cluster-2      rhel-6-lvs-1     rhevh-2  sam-1
  configure.ac  jboss-4           rhel-6-client-1       rhel-6-lvs-2     rhevm-1  satellite-1
  fedora-20-1   package.spec      rhel-6-cluster-1      rhel-6-lvs-rs-1  rhs-1    satellite6-1
  ipa-1         rhds-1            rhel-6-cluster-2      rhel-6-lvs-rs-2  rhs-2
  jboss-0       rhel-5-client-1   rhel-6-cluster-gfs-1  rhel-6-mrg-m-1   rhs-3
  jboss-1       rhel-5-client-2   rhel-6-cluster-gfs-2  rhel-6-mrg-m-2   rhs-4
  jboss-2       rhel-5-cluster-1  rhel-6-cluster-gfs-3  rhel-6-proxy-1   rpm.mk
  ssato@localhost% ls /tmp/w/guests.d/sam-1        ~/repos/public/github.com/ssato/miniascape.git
  Makefile  ks.cfg  net_register.sh  vmbuild.sh
  ssato@localhost% cat /tmp/w/guests.d/sam-1/vmbuild.sh
  #! /bin/bash
  # see also virt-install(1)
  #
  function genmac () { python -c 'from random import randint as f; print ":".join("%02x" % x for x in (0x52, 0x54, 0x00, f(0x00, 0x7f), f(0x00, 0xff),  f(0x00, 0xff)))'; }
  set -ex
  test $# -gt 0 && ks_path=$1 || ks_path=${0%/*}/ks.cfg
  kscfg=${ks_path##*/}
  name=default_sam-1
  connect=${QEMU_CONNECT:-qemu:///system}

  location_opts="--location=ftp://ftp.kddilabs.jp/Linux/packages/CentOS/6.5/os/x86_64/ --initrd-inject=${ks_path}"
  more_extra_args=""


  # Use virtio-scsi if available and there is a scsi disk:
  virtio_scsi_controller="--controller=scsi,model=virtio-scsi"

  virt-install \
  --check-cpu --hvm --accelerate --noreboot --noautoconsole \
  --name=${name:?} \
  --connect=${connect:?} \
  --wait=12 \
  --ram=2048 \
  --arch=x86_64 \
  --vcpus=2  \
  --graphics vnc \
  --os-type=linux \
  --os-variant=rhel6 \
  ${virtio_scsi_controller} \
  ${location_opts} --extra-args="ks=file:/${kscfg} ${more_extra_args}" \
  --disk pool=default,format=qcow2,cache=none,size=6,bus=scsi \
   \
  --network network=service,model=virtio,mac=52:54:00:05:00:15 \
  ssato@localhost% ls /tmp/w/host                  ~/repos/public/github.com/ssato/miniascape.git
  Makefile.am  configure.ac  etc  package.spec  rpm.mk  usr
  ssato@localhost% ls /tmp/w/host/usr/share/miniascape/networks.d/service.xml
  /tmp/w/host/usr/share/miniascape/networks.d/service.xml
  ssato@localhost% cat /tmp/w/host/usr/share/miniascape/networks.d/service.xml
  <network>
    <name>service</name>
    <forward mode='nat'/>
    <bridge name='virbr5' stp='on' delay='0' />
    <domain name='m2.local'/>
    <dns>
      <!-- Libvirt host aliases: -->
      <host ip='192.168.155.254'><hostname>gw.m2.local</hostname></host>
      <host ip='192.168.155.254'><hostname>ks.m2.local</hostname></host>
      <host ip='192.158.155.151'><hostname>rhel-5-client-1.m2.local</hostname></host>
      <host ip='192.158.155.152'><hostname>rhel-5-client-2.m2.local</hostname></host>
      <host ip='192.168.155.101'><hostname>rhel-5-cluster-1.m2.local</hostname></host>
      <host ip='192.168.155.102'><hostname>rhel-5-cluster-2.m2.local</hostname></host>
      <host ip='192.168.155.11'><hostname>satellite-1.m2.local</hostname></host>
      <host ip='192.168.155.111'><hostname>rhel-6-cluster-1.m2.local</hostname></host>
      <host ip='192.168.155.112'><hostname>rhel-6-cluster-2.m2.local</hostname></host>
      <host ip='192.168.155.113'><hostname>rhel-6-cluster-gfs-1.m2.local</hostname></host>
      <host ip='192.168.155.114'><hostname>rhel-6-cluster-gfs-2.m2.local</hostname></host>
      <host ip='192.168.155.115'><hostname>rhel-6-cluster-gfs-3.m2.local</hostname></host>
      <host ip='192.168.155.15'><hostname>sam-1.m2.local</hostname></host>
      <host ip='192.168.155.16'><hostname>satellite6-1.m2.local</hostname></host>
      <host ip='192.168.155.161'><hostname>rhel-6-client-1.m2.local</hostname></host>
      <host ip='192.168.155.17'><hostname>ipa-1.m2.local</hostname></host>
      <host ip='192.168.155.171'><hostname>rhel-6-lvs-1.m2.local</hostname></host>
      <host ip='192.168.155.172'><hostname>rhel-6-lvs-2.m2.local</hostname></host>
      <host ip='192.168.155.18'><hostname>rhds-1.m2.local</hostname></host>
      <host ip='192.168.155.181'><hostname>rhel-6-lvs-rs-1.m2.local</hostname></host>
      <host ip='192.168.155.182'><hostname>rhel-6-lvs-rs-2.m2.local</hostname></host>
      <host ip='192.168.155.191'><hostname>rhel-6-proxy-1.m2.local</hostname></host>
      <host ip='192.168.155.31'><hostname>rhevm-1.m2.local</hostname></host>
      <host ip='192.168.155.34'><hostname>rhevh-2.m2.local</hostname></host>
      <host ip='192.168.155.40'><hostname>jboss-0.m2.local</hostname></host>
      <host ip='192.168.155.41'><hostname>jboss-1.m2.local</hostname></host>
      <host ip='192.168.155.42'><hostname>jboss-2.m2.local</hostname></host>
      <host ip='192.168.155.43'><hostname>jboss-3.m2.local</hostname></host>
      <host ip='192.168.155.44'><hostname>jboss-4.m2.local</hostname></host>
      <host ip='192.168.155.51'><hostname>rhs-1.m2.local</hostname></host>
      <host ip='192.168.155.52'><hostname>rhs-2.m2.local</hostname></host>
      <host ip='192.168.155.53'><hostname>rhs-3.m2.local</hostname></host>
      <host ip='192.168.155.54'><hostname>rhs-4.m2.local</hostname></host>
      <host ip='192.168.155.71'><hostname>rhel-6-mrg-m-1.m2.local</hostname></host>
      <host ip='192.168.155.72'><hostname>rhel-6-mrg-m-2.m2.local</hostname></host>
    </dns>
    <ip address='192.168.155.254' netmask='255.255.255.0'>
      <dhcp>
        <range start='192.168.155.200' end='192.168.155.250'/>
        <host mac='52:54:00:05:00:11' name='satellite-1.m2.local' ip='192.168.155.11'/>
        <host mac='52:54:00:05:00:15' name='sam-1.m2.local' ip='192.168.155.15'/>
        <host mac='52:54:00:05:00:16' name='satellite6-1.m2.local' ip='192.168.155.16'/>
        <host mac='52:54:00:05:00:17' name='ipa-1.m2.local' ip='192.168.155.17'/>
        <host mac='52:54:00:05:00:18' name='rhds-1.m2.local' ip='192.168.155.18'/>
        <host mac='52:54:00:05:00:31' name='rhevm-1.m2.local' ip='192.168.155.31'/>
        <host mac='52:54:00:05:00:34' name='rhevh-2.m2.local' ip='192.168.155.34'/>
        <host mac='52:54:00:05:00:40' name='jboss-0.m2.local' ip='192.168.155.40'/>
        <host mac='52:54:00:05:00:41' name='jboss-1.m2.local' ip='192.168.155.41'/>
        <host mac='52:54:00:05:00:42' name='jboss-2.m2.local' ip='192.168.155.42'/>
        <host mac='52:54:00:05:00:43' name='jboss-3.m2.local' ip='192.168.155.43'/>
        <host mac='52:54:00:05:00:44' name='jboss-4.m2.local' ip='192.168.155.44'/>
        <host mac='52:54:00:05:00:51' name='rhs-1.m2.local' ip='192.168.155.51'/>
        <host mac='52:54:00:05:00:52' name='rhs-2.m2.local' ip='192.168.155.52'/>
        <host mac='52:54:00:05:00:53' name='rhs-3.m2.local' ip='192.168.155.53'/>
        <host mac='52:54:00:05:00:54' name='rhs-4.m2.local' ip='192.168.155.54'/>
        <host mac='52:54:00:05:00:71' name='rhel-6-mrg-m-1.m2.local' ip='192.168.155.71'/>
        <host mac='52:54:00:05:00:72' name='rhel-6-mrg-m-2.m2.local' ip='192.168.155.72'/>
        <host mac='52:54:00:05:01:01' name='rhel-5-cluster-1.m2.local' ip='192.168.155.101'/>
        <host mac='52:54:00:05:01:02' name='rhel-5-cluster-2.m2.local' ip='192.168.155.102'/>
        <host mac='52:54:00:05:01:11' name='rhel-6-cluster-1.m2.local' ip='192.168.155.111'/>
        <host mac='52:54:00:05:01:12' name='rhel-6-cluster-2.m2.local' ip='192.168.155.112'/>
        <host mac='52:54:00:05:01:13' name='rhel-6-cluster-gfs-1.m2.local' ip='192.168.155.113'/>
        <host mac='52:54:00:05:01:14' name='rhel-6-cluster-gfs-2.m2.local' ip='192.168.155.114'/>
        <host mac='52:54:00:05:01:15' name='rhel-6-cluster-gfs-3.m2.local' ip='192.168.155.115'/>
        <host mac='52:54:00:05:01:51' name='rhel-5-client-1.m2.local' ip='192.158.155.151'/>
        <host mac='52:54:00:05:01:52' name='rhel-5-client-2.m2.local' ip='192.158.155.152'/>
        <host mac='52:54:00:05:01:61' name='rhel-6-client-1.m2.local' ip='192.168.155.161'/>
        <host mac='52:54:00:05:01:71' name='rhel-6-lvs-1.m2.local' ip='192.168.155.171'/>
        <host mac='52:54:00:05:01:72' name='rhel-6-lvs-2.m2.local' ip='192.168.155.172'/>
        <host mac='52:54:00:05:01:81' name='rhel-6-lvs-rs-1.m2.local' ip='192.168.155.181'/>
        <host mac='52:54:00:05:01:82' name='rhel-6-lvs-rs-2.m2.local' ip='192.168.155.182'/>
        <host mac='52:54:00:05:01:91' name='rhel-6-proxy-1.m2.local' ip='192.168.155.191'/>
      </dhcp>
    </ip>
  </network>%                                                                                     ssato@localhost% ls /tmp/w/host                  ~/repos/public/github.com/ssato/miniascape.git
  Makefile.am  configure.ac  etc  package.spec  rpm.mk  usr
  ssato@localhost% (cd /tmp/w/host; autoreconf -vfi; ./configure ; make rpm)
  autoreconf: Entering directory `.'
  autoreconf: configure.ac: not using Gettext
  autoreconf: running: aclocal --force
  autoreconf: configure.ac: tracing
  autoreconf: configure.ac: not using Libtool
  autoreconf: running: /usr/bin/autoconf --force
  autoreconf: configure.ac: not using Autoheader
  autoreconf: running: automake --add-missing --copy --force-missing
  configure.ac:2: installing './install-sh'
  configure.ac:2: installing './missing'
  autoreconf: Leaving directory `.'
  checking for a BSD-compatible install... /usr/bin/install -c
  checking whether build environment is sane... yes
  checking for a thread-safe mkdir -p... /usr/bin/mkdir -p
  checking for gawk... gawk
  checking whether make sets $(MAKE)... yes
  checking whether make supports nested variables... yes
  checking how to create a pax tar archive... gnutar
  checking whether make supports nested variables... (cached) yes
  checking that generated files are newer than configure... done
  configure: creating ./config.status
  config.status: creating Makefile
  make  dist-xz am__post_remove_distdir='@:'
  make[1]: ディレクトリ `/tmp/w/host' に入ります
  if test -d "miniascape-host-data-default-0.0.1"; then find "miniascape-host-data-default-0.0.1" -type d ! -perm -200 -exec chmod u+w {} ';' && rm -rf "miniascape-host-data-default-0.0.1" || { sleep 5 && rm -rf "miniascape-host-data-default-0.0.1"; }; else :; fi
  test -d "miniascape-host-data-default-0.0.1" || mkdir "miniascape-host-data-default-0.0.1"
  test -n "" \
  || find "miniascape-host-data-default-0.0.1" -type d ! -perm -755 \
          -exec chmod u+rwx,go+rx {} \; -o \
    ! -type d ! -perm -444 -links 1 -exec chmod a+r {} \; -o \
    ! -type d ! -perm -400 -exec chmod a+r {} \; -o \
    ! -type d ! -perm -444 -exec /bin/sh /tmp/w/host/install-sh -c -m a+r {} {} \; \
  || chmod -R a+r "miniascape-host-data-default-0.0.1"
  tardir=miniascape-host-data-default-0.0.1 && tar --format=posix -chf - "$tardir" | XZ_OPT=${XZ_OPT--e} xz -c >miniascape-host-data-default-0.0.1.tar.xz
  make[1]: ディレクトリ `/tmp/w/host' から出ます
  if test -d "miniascape-host-data-default-0.0.1"; then find "miniascape-host-data-default-0.0.1" -type d ! -perm -200 -exec chmod u+w {} ';' && rm -rf "miniascape-host-data-default-0.0.1" || { sleep 5 && rm -rf "miniascape-host-data-default-0.0.1"; }; else :; fi
    GEN      rpm
  configure: WARNING: unrecognized options: --disable-dependency-tracking
  configure: WARNING: unrecognized options: --disable-dependency-tracking
  ssato@localhost% rpm -qlp /tmp/w/host/miniascape-host-data-default-0.0.1-1.fc20.noarch.rpm
  /usr/share/miniascape/networks.d/default.xml
  /usr/share/miniascape/networks.d/service.xml
  ssato@localhost% ls /tmp/w/host                  ~/repos/public/github.com/ssato/miniascape.git
  Makefile        install-sh
  Makefile.am     miniascape-host-data-common-0.0.1-1.fc20.noarch.rpm
  Makefile.in     miniascape-host-data-default-0.0.1-1.fc20.noarch.rpm
  aclocal.m4      miniascape-host-data-default-0.0.1.tar.xz
  autom4te.cache  miniascape-host-data-default-overrides-0.0.1-1.fc20.noarch.rpm
  config.log      missing
  config.status   package.spec
  configure       rpm
  configure.ac    rpm.mk
  etc             usr
  ssato@localhost%                                 ~/repos/public/github.com/ssato/miniascape.git

Once ks.cfg and vm build script are dumped, just run it to build VMs like this.

::

  ssato@localhost% sudo bash -x /tmp/w/guests.d/sam/vmbuild.sh
  + set -ex
  + test 0 -gt 0
  + ks_path=./workdir-20120921/guests.d/sam/ks.cfg
  + kscfg=ks.cfg
  + location=http://ks.m2.local/contents/RHEL/6/3/x86_64/default/
  + virt-install --check-cpu --hvm --accelerate --noreboot --noautoconsole --name=sam --connect=qemu:///system --wait=20 --ram=2048 --arch=x86_64 --vcpus=2 --graphics vnc --os-type=linux --os-variant=rhel6 --location=http://ks.m2.local/contents/RHEL/6/3/x86_64/default/ --initrd-inject=./workdir-20120921/guests.d/sam/ks.cfg --disk pool=default,format=qcow2,cache=none,size=5 --network network=service,model=virtio,mac=52:54:00:05:00:15 '--extra-args=ks=file:/ks.cfg ksdevice=eth0 '

  Starting install...
  Retrieving file vmlinuz...                                    | 7.6 MB     00:00 !!!
  Retrieving file initrd.img...                                 |  58 MB     00:00 !!!
  Allocating 'sam-2.img'                                        | 5.0 GB     00:00
  Creating domain...                                            |    0 B     00:00
  Domain installation still in progress. Waiting 20 minutes for installation to complete.
  ssato@localhost%

.. vim:sw=2:ts=2:et:

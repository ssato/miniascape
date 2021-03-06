#! /bin/bash
set -ex

curdir=${0%/*}
topdir=${curdir}/../

workdir=$(mktemp -d /tmp/m2.XXXXXXXXXX)
cleanup () { rm -rf ${workdir}; }

trap cleanup INT TERM

for site in default hacluster openshift openstack rhui; do
  anyconfig_cli -vv --template "conf/${site}/"'*.yml' -o ${workdir}/conf.yml \
    2>&1 | tee ${workdir}/conf.${site}.log

  PYTHONPATH=${topdir} python miniascape/cli.py b \
    -t ${topdir}/templates -C conf/${site}/ -w ${workdir}
done

# check w/ ksvalidator:
for f in ${workdir}/guests.d/rhel-5-*/ks.cfg; do ksvalidator -e -v RHEL5 $f; done
for f in ${workdir}/guests.d/rhel-6-*/ks.cfg; do ksvalidator -e -v RHEL6 $f; done
for f in ${workdir}/guests.d/{rhel-7-,jboss,satellite6}*/ks.cfg; do
  # quick and dirty hack; ksvalidator does not look support '%addon'.
  sed -i '/^%addon/,/%end/d' $f
  ksvalidator -e -v RHEL7 $f
done
for f in ${workdir}/guests.d/ose*/ks.cfg; do ksvalidator -e -v RHEL7 $f; done
for f in ${workdir}/guests.d/{rhua,cds}*/ks.cfg; do ksvalidator -e -v RHEL6 $f; done

cleanup

# vim:sw=2:ts=2:et:

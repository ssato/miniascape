#! /bin/bash
set -ex

curdir=${0%/*}
topdir=${curdir}/../

workdir=$(mktemp -d /tmp/m2.XXXXXXXXXX)
cleanup () { rm -rf ${workdir}; }

trap cleanup INT TERM

for site in default openstack rhui; do
  PYTHONPATH=${topdir} python miniascape/cli.py b \
    -t ${topdir}/templates -C conf/${site}/ -w ${workdir}
done

# check w/ ksvalidator:
for f in ${workdir}/guests.d/rhel-5-*/ks.cfg; do ksvalidator -e -v RHEL5 $f; done
for f in ${workdir}/guests.d/{rhel-6-,jboss}*/ks.cfg; do ksvalidator -e -v RHEL6 $f; done

cleanup

# vim:sw=2:ts=2:et:

#! /bin/bash
set -ex

curdir=${0%/*}
topdir=${curdir}/../

workdir=$(mktemp -d)

trap "rm -rf ${workdir}" INT TERM EXIT

for site in default openstack rhui; do
  PYTHONPATH=${topdir} python miniascape/cli.py b \
    -t ${topdir}/templates -s ${site} \
    -C "conf/${site}/\*.yml" -w ${workdir}
done

# vim:sw=2:ts=2:et:

#! /bin/bash
set -e

curdir=${0%/*}
topdir=${curdir}/../

PYTHONPATH=${topdir} python miniascape/cli.py b \
  -t ${topdir}/templates -s default \
  -C 'conf/default/*.yml' -w /tmp/w -v

# vim:sw=2:ts=2:et:

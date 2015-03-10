#! /bin/bash
set -e

curdir=${0%/*}
topdir=${curdir}/../
mergetool=${topdir}/tools/miniascape-mergeconfs.sh

for d in ${topdir}/conf/*/*.yml.d/; do ${mergetool} ${d}; done

# vim:sw=4:ts=4:et:

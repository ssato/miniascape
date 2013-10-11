#! /bin/bash
curdir=${0%/*}
topdir=${curdir}/../

workdir=$(mktemp -d /tmp/miniascape-XXXXXXXXXX)

(cd ${topdir} && \
 PYTHONPATH=. python tools/miniascape ge -t ./templates -w ${workdir} -c ./default)

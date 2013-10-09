#! /bin/bash
curdir=${0%/*}
topdir=${curdir}/../

(cd ${topdir} && \
 PYTHONPATH=. python tools/miniascape c -t ./templates -w ./ -c ./default/src.d/00_base.yml)

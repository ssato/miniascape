#! /bin/bash
curdir=${0%/*}
topdir=${curdir}/../

(cd ${topdir} && \
 PYTHONPATH=. python tools/miniascape c -f -t ./templates -w ./conf -c ./conf/default/src.d)

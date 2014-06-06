#! /bin/bash
curdir=${0%/*}
topdir=${curdir}/../

(cd ${topdir} && \
for d in ./conf/*/src.d; do \
  PYTHONPATH=. python tools/miniascape c -f -t ./templates -w ./conf -c $d; \
done)

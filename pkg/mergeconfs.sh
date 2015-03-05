#! /bin/bash
set -ex

curdir=${0%/*}
topdir=${curdir}/../

for d in ${topdir}/conf/*/*.yml.d/; do
    for f in ${d}/*.yml; do
        out=${f/\.d\/*/}
        outtmp=${out}.t
        sed -n '/^#/d; p' $f >> ${outtmp}
    done
    test -f ${outtmp} && mv ${outtmp} ${out}
done

# vim:sw=4:ts=4:et:

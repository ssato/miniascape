#! /bin/bash
set -e

curdir=${0%/*}
topdir=${curdir}/../

for d in ${topdir}/conf/*/*.yml.d/; do
    echo -ne "[Info] Merge files in ${d}: "
    for f in ${d}/*.yml; do
        out=${f/\.d\/*/}
        outtmp=${out}.t
        sed -n '/^#/d; p' $f >> ${outtmp}
    done
    test -f ${outtmp} && mv ${outtmp} ${out} || :
    echo "Done"
done

# vim:sw=4:ts=4:et:

#! /bin/bash
set -e

curdir=${0%/*}
topdir=${curdir}/../
targets="
templates/autoinstall.d/snippets/pre.store_cmdline
"

workdir=${1:-$(mktemp -d)}
test -d ${workdir:?} || mkdir -p ${workdir}

for t in ${targets}; do
    ttdir=${curdir}/${t}.d
    tt=${topdir}/${t}

    for f in ${ttdir}/*_input; do
        bf=${f##*/}
        output=${workdir}/${bf/input/output}
        exp=${f/input/output.exp}

        bash ${tt} ${output} ${f}
        diff -u ${exp} ${output}
    done
    rm -rf ${workdir:?}
done
# vim:sw=4:ts=4:et:

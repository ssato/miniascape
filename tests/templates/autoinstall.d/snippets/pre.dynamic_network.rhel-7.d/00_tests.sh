#! /bin/bash
#set -e

curdir=${0%/*}
tt="pre.dynamic_network.rhel-7"

workdir=${1:-$(mktemp -d)}
test -d ${workdir:?} || mkdir -p ${workdir}

# Hack:
cp ${curdir}/pre.dynamic_network.rhel-7.functions ${workdir}/
sed '1s/.*/source pre.dynamic_network.rhel-7.functions/' ${curdir}/${tt} > ${workdir}/${tt}

cd ${curdir}
for f in *_input; do

    bf=${f##*/}
    output=${workdir}/${bf/input/output}
    exp=${f/input/output.exp}

    bash ${workdir}/${tt} ${bf} ${workdir} ${output} > ${workdir}/run.log
    t_result=$(diff -u ${exp} ${output}); t_rc=$?
    if test ${t_rc} -eq 0; then
        echo "OK: ${bf}"
    else
        echo "NG: ${bf}"
        echo "-------------------------------------------"
        echo "${t_result}"
        echo "-------------------------------------------"
    fi
done
rm -rf ${workdir:?}

# vim:sw=4:ts=4:et:

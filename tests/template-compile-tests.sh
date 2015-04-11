#! /bin/bash
#set -e

curdir=${0%/*}
topdir=${curdir}/../
targets="
$(sed '/^#.*/d' ${curdir}/template-compile-tests.targets)
"

for tgt in ${targets}; do
    workdir=${1:-$(mktemp -d)}
    test -d ${workdir:?} || mkdir -p ${workdir}

    tmpl_test_datadir=${curdir}/${tgt}.d
    tmpl=${topdir}/${tgt}

    ng_cnt=0

    for ctx_f in ${tmpl_test_datadir}/*_ctx.yml; do
        test_basename=${ctx_f##*/}
        test_basename=${test_basename/_ctx.yml/}
        exp_f=${tmpl_test_datadir}/${test_basename}_out.exp
        out_f=${workdir}/${test_basename}_out
        err_f=${workdir}/${test_basename}_err

        jinja2-cli r -C ${ctx_f} -T ${topdir}/templates/autoinstall.d -o ${out_f} ${tmpl} 2> ${err_f}
        test_result=$(diff -u ${exp_f} ${out_f}); test_rc=$?
        if test ${test_rc} -ne 0; then
            echo "NG: ${test_basename}, see the log ${err_f} for more details:"
            echo "-------------------------------------------"
            echo "${test_result}"
            echo "-------------------------------------------"
            ng_cnt=$(( ${ng_cnt} + 1 ))
        fi
    done
    tmpl=${tmpl/*templates\/}
    echo "${tmpl}: "$(test ${ng_cnt} -eq 0 && (echo 'OK'; rm -rf ${workdir:?}) || echo "NG [${ng_cnt}]")
done

# vim:sw=4:ts=4:et:

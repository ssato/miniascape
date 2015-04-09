#! /bin/bash
#set -e

curdir=${0%/*}
targets="
templates/autoinstall.d/snippets/pre.dynamic_network.rhel-7.functions
"

for t in ${targets}; do
    ttdir=${curdir}/${t}.d

    for f in ${ttdir}/*_tests.sh; do
        bash ${f} && res=OK || res=NG
        echo "${f/tests\/templates}: ${res} -----------------------"
    done
done

# vim:sw=4:ts=4:et:

#! /bin/bash
set -e
curdir=${0%/*}
topdir=${curdir}/../
testsdir=${topdir}/tests/

${testsdir}/template-run-tests.sh
${testsdir}/template-run-unittests.sh

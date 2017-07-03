#! /bin/bash
#
# Create and setup activation keys
#
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
set -ex

# HAMMER_ORG_ID_OPT, PRODUCTS_TO_SYNC, REPOS_TO_SYNC
source ${0%/*}/config.sh

while read line; do
  test "x$line" = "x" || (
  hammer product synchronize ${HAMMER_ORG_ID_OPT} --name "${line}" --async
done << EOC
${PRODUCTS_TO_SYNC:?}
EOC

# TODO:
#while read line; do
#  test "x$line" = "x" || (
#  hammer product synchronize ${HAMMER_ORG_ID_OPT} ${line} --async
#done << EOC
#${REPOS_TO_SYNC:?}
#EOC

# vim:sw=2:ts=2:et:

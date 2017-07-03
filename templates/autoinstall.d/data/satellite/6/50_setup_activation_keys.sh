#! /bin/bash
#
# Create and setup activation keys
#
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
set -ex

# HAMMER_ORG_ID_OPT, CREATE_ACTIVATION_KEYS,
# ADD_HOST_COLLECTION_TO_ACTIVATION_KEYS, ADD_SUBSCRIPTION_TO_ACTIVATION_KEYS
source ${0%/*}/config.sh

hammer --csv activation-key list ${HAMMER_ORG_ID_OPT:?} | grep -E '^1,' || (
while read line; do test "x$line" = "x" || (eval "${line}" || :); done << EOC
${CREATE_ACTIVATION_KEYS:?}
EOC

while read line; do test "x$line" = "x" || (eval ${line} || :); done << EOC
${ADD_HOST_COLLECTION_TO_ACTIVATION_KEYS:?}
EOC

while read line; do test "x$line" = "x" || (eval ${line} || :); done << EOC
${ADD_SUBSCRIPTION_TO_ACTIVATION_KEYS:?}
EOC
)

# vim:sw=2:ts=2:et:
{#
#}

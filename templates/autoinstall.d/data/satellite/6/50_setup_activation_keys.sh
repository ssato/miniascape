#! /bin/bash
#
# Create and setup activation keys
#
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
set -ex

# HAMMER_ORG_ID_OPT, ACTIVATION_KEYS, ACTIVATION_KEYS_WITH_HOST_COLLECTIONS,
# ACTIVATION_KEYS_WITH_SUBSCRIPTIONS
source ${0%/*}/config.sh

hammer --csv activation-key list ${HAMMER_ORG_ID_OPT:?} | grep -E '^1,' || (
while read line; do
  test "x$line" = "x" || (
  hammer activation-key create ${HAMMER_ORG_ID_OPT} ${line}
  )
done << EOC
${ACTIVATION_KEYS:?}
EOC

while read line; do
  test "x$line" = "x" || (
  hammer activation-key add-host-collection ${HAMMER_ORG_ID_OPT} ${line} || :
  )
done << EOC
${ACTIVATION_KEYS_WITH_HOST_COLLECTIONS:?}
EOC

while read line; do
  test "x$line" = "x" || (
  hammer activation-key add-subscription ${HAMMER_ORG_ID_OPT} ${line} || :
  )
done << EOC
${ACTIVATION_KEYS_WITH_SUBSCRIPTIONS:?}
EOC
)

# vim:sw=2:ts=2:et:
{#
#}

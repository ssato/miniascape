#! /bin/bash
#
# Setup Host Collections, Lifecycle Environments and Content views.
#   - Setup Host Collection: hammer host-collection create
#   - Setup Lifecycle Environments: hammer lifecycle-environment create
#   - Setup Content View [option]: hammer content-view create, hammer content-view add-repository
#
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
set -ex

# HAMMER_ORG_ID_OPT, HOST_COLLECTIONS, LIFECYCLE_ENVIRONMENTS, CONTENT_VIEWS,
# CONTENT_VIEWS_WITH_REPOS
source ${0%/*}/config.sh

# Create Host Collections
hammer host-collection list ${HAMMER_ORG_ID_OPT:?} | grep -qE '^1,' || (
while read line; do
  test "x$line" = "x" || (
  hammer host-collection create ${HAMMER_ORG_ID_OPT} ${line} || :
  )
done << EOC
${HOST_COLLECTIONS:?}
EOC
)

# Create Lifecycle Environments
hammer lifecycle-environment list ${HAMMER_ORG_ID_OPT:?} | grep -qE '^1,' || (
while read line; do
  test "x$line" = "x" || (
  hammer lifecycle-environment create ${HAMMER_ORG_ID_OPT} ${line} || :
  )
done << EOC
${LIFECYCLE_ENVIRONMENTS:?}
EOC
)

# Create and setup Content Views
hammer content-view list ${HAMMER_ORG_ID_OPT:?} | grep -qE '^2,' || (
while read line; do
  test "x$line" = "x" || (
  hammer content-view create ${HAMMER_ORG_ID_OPT} ${line} || :
  )
done << EOC
${CONTENT_VIEWS:?}
EOC
while read line; do
  test "x$line" = "x" || (
  hammer content-view add-repository ${HAMMER_ORG_ID_OPT} ${line} || :
  )
done << EOC
${CONTENT_VIEWS_WITH_REPOS:?}
EOC
)

# vim:sw=2:ts=2:et:
{#
#}

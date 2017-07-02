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

# Create and setup Host Collections
while read line; do
  test "x$line" = "x" || (
  hammer host-collection create ${HAMMER_ORG_ID_OPT:?} --name "${name}" ${opts}
  )
done << EOC
${HOST_COLLECTIONS:?}
EOC

# Create and setup Lifecycle Environments
while read line; do
  test "x$line" = "x" || (
  name=${line%% *}; opts=${line#* }
  hammer lifecycle-environment create ${HAMMER_ORG_ID_OPT} --name "${name}" ${opts}
  )
done << EOC
${LIFECYCLE_ENVIRONMENTS:?}
EOC

# Create and setup Content Views
while read line; do
  test "x$line" = "x" || (
  name=${line%% *}; opts=${line#* }
  hammer content-view create ${HAMMER_ORG_ID_OPT} --name "${name}" ${opts}
  )
done << EOC
${CONTENT_VIEWS:?}
EOC
while read line; do
  test "x$line" = "x" || (
  name=${line%% *}; opts=${line#* }
  hammer content-view add-repository ${HAMMER_ORG_ID_OPT} --name "${name}" ${opts}
  )
done << EOC
${CONTENT_VIEWS_WITH_REPOS:?}
EOC

# vim:sw=2:ts=2:et:

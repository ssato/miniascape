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

# CREATE_HOST_COLLECTIONS, CREATE_LIFECYCLE_ENVIRONMENTS,
# CREATE_CONTENT_VIEWS, ADD_REPOS_TO_CONTENT_VIEWS
source ${0%/*}/config.sh

# Create Host Collections
hammer host-collection list | grep -qE '^1,' || (
while read line; do test "x$line" = "x" || (eval ${line} || :); done << EOC
${CREATE_HOST_COLLECTIONS:?}
EOC
)
hammer --csv host-collection list

# Create Lifecycle Environments
hammer lifecycle-environment list | grep -qE '^1,' || (
while read line; do test "x$line" = "x" || (eval ${line} || :); done << EOC
${CREATE_LIFECYCLE_ENVIRONMENTS:?}
EOC
)
hammer --csv lifecycle-environment list

# Create and setup Content Views
hammer content-view list | grep -qE '^2,' || (
while read line; do test "x$line" = "x" || (eval ${line} || :); done << EOC
${CREATE_CONTENT_VIEWS:?}
EOC
while read line; do test "x$line" = "x" || (eval ${line} || :); done << EOC
${ADD_REPOS_TO_CONTENT_VIEWS:?}
EOC
)
hammer --csv content-view list

# vim:sw=2:ts=2:et:
{#
#}

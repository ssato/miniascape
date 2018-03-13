#! /bin/bash
#
# Setup Yum Repos
#   - Enable Yum repos: hammer repository-set enable
#   - Setup Sync Plan:
#     - online: hammer sync-plan create --enabled true
#     - offline: hammer sync-plan create --enabled false [default]
#
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
set -ex

# CURL_PROXY_OPT, ENABLE_YUM_REPOS_FOR_CLIENTS, PRODUCTS
source ${0%/*}/config.sh

# Check if satellite host can access RH CDN.
curl --connect-timeout 10 --cacert /etc/rhsm/ca/redhat-uep.pem ${CURL_PROXY_OPT} https://cdn.redhat.com/

_PROCUCTS_REPOS_ENABLED_FOR_CLIENTS="$(cat << EOC | sort | uniq
${PROCUCTS_REPOS_ENABLED_FOR_CLIENTS}
EOC
)
"

# List products and repository-sets (all available repos) by products.
hammer --csv product list --by name
while read line; do test "x$line" = "x" || hammer --csv repository-set list --product "$line"; done << EOC
${_PROCUCTS_REPOS_ENABLED_FOR_CLIENTS}
EOC

# Enable Yum repos will be provided for clients
while read line; do test "x$line" = "x" || (eval ${line} || :); done << EOC
${ENABLE_YUM_REPOS_FOR_CLIENTS:?}
EOC

# List repositories (enabled repos) by products.
while read line; do test "x$line" = "x" || hammer --csv repository list --product "$line" --by name; done << EOC
${_PROCUCTS_REPOS_ENABLED_FOR_CLIENTS}
EOC

# Create and setup sync plans if not yet
hammer sync-plan info --name 'Daily Sync' 2> /dev/null || (
hammer sync-plan create --interval daily --name 'Daily Sync' --enabled true --sync-date "$(date --iso-8601=minutes --date '6 hour')"
while read line; do
    test "x$line" = "x" || (
    hammer product set-sync-plan --name "${line}" --sync-plan "Daily Sync" || :
    )
done << EOC
${PRODUCTS:?}
EOC
)

# vim:sw=4:ts=4:et:
{#
#}

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

# CURL_PROXY_OPT, HAMMER_ORG_ID_OPT, YUM_REPOS_FOR_CLIENTS, PRODUCTS
source ${0%/*}/config.sh

# Check if satellite host can access RH CDN.
curl ${CURL_PROXY_OPT} https://cdn.redhat.com

# Customize SELinux policy to allow proxy access
tweak_selinux_policy

# Enable Yum repos will be provided for clients
while read line; do
    test "x$line" = "x" || (
    name=${line%% *}; opts=${line#* }
    hammer repository-set enable ${HAMMER_ORG_ID_OPT} --name "${name}" ${opts}
    )
done << EOC
${YUM_REPOS_FOR_CLIENTS=:?}
EOC

# Create and setup sync plans if not yet
hammer sync-plan info ${HAMMER_ORG_ID_OPT:?} --name 'Daily Sync' 2> /dev/null || \
hammer sync-plan create ${HAMMER_ORG_ID_OPT} --interval daily --name 'Daily Sync' --enabled true --sync-date "$(date --iso-8601=minutes --date '6 hour')"

# Set sync plan for products
while read line; do
    test "x$line" = "x" || (
    hammer product set-sync-plan ${HAMMER_ORG_ID_OPT} --name "${line}" --sync-plan "Daily Sync"
    )
done << EOC
${PRODUCTS:?}
EOC

# vim:sw=4:ts=4:et:

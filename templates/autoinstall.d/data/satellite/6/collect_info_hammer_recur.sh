#! /bin/bash
#
# A shell script to collect help texts of hammer's commands recursively.
#
# Author: Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# Examples:
#
# [root@sat01 ~]# o=$(hammer subscription --help); list_subcmds_0 "$o"
# delete-manifest
# list
# manifest-history
# refresh-manifest
# upload
# [root@sat01 ~]# echo "$o"
# Usage:
#     hammer subscription [OPTIONS] SUBCOMMAND [ARG] ...
# 
# Parameters:
#  SUBCOMMAND                    subcommand
#  [ARG] ...                     subcommand arguments
# 
# Subcommands:
#  delete-manifest               Delete manifest from Red Hat provider
#  list                          List organization subscriptions
#  manifest-history              obtain manifest history for subscriptions
#  refresh-manifest              Refresh previously imported manifest for Red Hat provider
#  upload                        Upload a subscription manifest
# 
# Options:
#  -h, --help                    print help
# [root@sat01 ~]#
#
# [root@sat01 ~]# list_subcmds_recur hammer subscription
# hammer subscription
# Usage:
#     hammer subscription [OPTIONS] SUBCOMMAND [ARG] ...
# 
# Parameters:
#  SUBCOMMAND                    subcommand
#  [ARG] ...                     subcommand arguments
# 
# Subcommands:
#  delete-manifest               Delete manifest from Red Hat provider
#  list                          List organization subscriptions
#  manifest-history              obtain manifest history for subscriptions
#  refresh-manifest              Refresh previously imported manifest for Red Hat provider
#  upload                        Upload a subscription manifest
# 
# Options:
#  -h, --help                    print help
# # hammer subscription delete-manifest
# Usage:
#     hammer subscription delete-manifest [OPTIONS]
# 
# Options:
#  --async                                 Do not wait for the task
#  --content-host CONTENT_HOST_NAME        Name to search by
#  --content-host-id CONTENT_HOST_ID       UUID of the content host
#  --organization ORGANIZATION_NAME        Organization name to search by
#  --organization-id ORGANIZATION_ID       organization ID
#  --organization-label ORGANIZATION_LABEL Organization label to search by
#  -h, --help                              print help
# # hammer subscription list
# Usage:
#     hammer subscription list [OPTIONS]
# 
# Options:
#  --activation-key ACTIVATION_KEY_NAME    Activation key name to search by
#  --activation-key-id ACTIVATION_KEY_ID   ID of the activation key
#  --available-for AVAILABLE_FOR           Object to show subscriptions available for, either 'host' or
#                                          'activation_key'
#  --by BY                                 Field to sort the results on
#  --full-results FULL_RESULTS             Whether or not to show all results
#                                          One of true/false, yes/no, 1/0.
#  --host HOST_NAME                        Name to search by
#  --host-id HOST_ID
#  --match-host MATCH_HOST                 Ignore subscriptions that are unavailable to the specified host
#                                          One of true/false, yes/no, 1/0.
#  --match-installed MATCH_INSTALLED       Return subscriptions that match installed products of the specified host
#                                          One of true/false, yes/no, 1/0.
#  --no-overlap NO_OVERLAP                 Return subscriptions which do not overlap with a currently-attached
#                                          subscription
#                                          One of true/false, yes/no, 1/0.
#  --order ORDER                           Sort field and order, eg. 'name DESC'
#  --organization ORGANIZATION_NAME        Organization name to search by
#  --organization-id ORGANIZATION_ID       organization ID
#  --organization-label ORGANIZATION_LABEL Organization label to search by
#  --page PAGE                             Page number, starting at 1
#  --per-page PER_PAGE                     Number of results per page to return
#  --search SEARCH                         Search string
#  -h, --help                              print help
#	... (snip) ...
set -e

list_subcmds_from_out () {
    test "x$@" = "x" || echo "$@" | \
        sed -nr '/Subcommands:/,/Options:/{s/[[:blank:]]+([a-z_-]+)[[:blank:]]+.*/\1/p}'
}
list_subcmds_recur () {
    local sc=$@
    local help=$($sc --help)
    local scs=$(list_subcmds_from_out "$help")
    echo "# $sc"; echo "$help"
    for ssc in $scs; do list_subcmds_recur $sc $ssc; done
}

list_subcmds_recur ${@:-hammer}

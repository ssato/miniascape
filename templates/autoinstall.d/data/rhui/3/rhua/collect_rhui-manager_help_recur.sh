#! /bin/bash
#
# A script to collect help texts of rhui-manager's commands recursively.
#
# Author: Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# Usage: ./collect_rhui-manager_help_recur.sh
#
# Example:
#
# [root@rhui-2 ~]# ./collect_rhui-manager_help_recur.sh
# rhui-manager
# Usage: rhui-manager [options] [command]
# 
#   OPTIONS
#     -h/--help  show this help message and exit
#     --debug    enables debug logging
#     --config   absolute path to the configuration file; defaults to /etc/rhui/rhui.conf
#     --server   location of the RHUA server (overrides the config file)
#     --username if specified, previously saved authentication credentials are ignored and this username is used to login
#     --password used in conjunction with --username
# 
#   COMMANDS
#     cert      : Red Hat content certificate management
#     packages  : package manipulation on repositories
#     repo      : repository listing and manipulation
#     status    : RHUI status and health information
#     cds       : associated cds commands
#     client    : Red Hat client management
# 
# Options:
# # rhui-manager cert
# Red Hat content certificate management
#     info      : display information about the current content certificate
#     upload    : uploads a new content certificate
#     repair    : reloads a content certificate
# # rhui-manager cert info
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help  show this help message and exit
# info: display information about the current content certificate
# # rhui-manager cert upload
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help     show this help message and exit
# upload: uploads a new content certificate
#     --cert - full path to the new content certificate (required)
#     --key - full path to the new content certificate's key
# # rhui-manager cert repair
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help       show this help message and exit
# repair: reloads a content certificate
#     --cert - full path to the new content certificate
#     --key - full path to the new content certificate's key
#     --force - force a repair, to be used w/ --cert and --key
# # rhui-manager packages
# package manipulation on repositories
#     upload    : uploads a package or directory of packages to a repository
#     list      : lists all packages in a repository
# # rhui-manager packages upload
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help            show this help message and exit
# upload: uploads a package or directory of packages to a repository
#     --repo_id - id of the repository where the packages will be uploaded (required)
#     --packages - path to an .rpm file or directory of RPMs that will be uploaded (required)
# # rhui-manager packages list
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help           show this help message and exit
# list: lists all packages in a repository
#     --repo_id - id of the repository to list packages for (required)
# # rhui-manager repo
# repository listing and manipulation
#     list      : lists all repositories in the RHUI
#     info      : displays information on an individual repo
#     add       : add a Red Hat respository to the RHUA
#     sync      : sync a repository
#     unused    : list of products available but not synced to the RHUA
# # rhui-manager repo list
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help  show this help message and exit
# list: lists all repositories in the RHUI
# # rhui-manager repo info
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help           show this help message and exit
# info: displays information on an individual repo
#     --repo_id - identifies the repository to display (required)
# # rhui-manager repo add
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help            show this help message and exit
# add: add a Red Hat respository to the RHUA
#     --product_name - repository id to add the RHUA (required)
# # rhui-manager repo sync
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help           show this help message and exit
# sync: sync a repository
#     --repo_id - identifies the repository to display (required)
# # rhui-manager repo unused
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help  show this help message and exit
# unused: list of products available but not synced to the RHUA
# # rhui-manager status
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help  show this help message and exit
# status: RHUI status and health information
#     --code - if specified, only a numeric code for the result will be displayed
# # rhui-manager cds
# associated cds commands
#     available : list of cds servers available to sync
#     sync      : sync content to specified cds
#     associate : associate a repo with a cds
#     clusters  : list of cds clusters
#     repos     : list of repositories for provided cluster
# # rhui-manager cds available
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help  show this help message and exit
# available: list of cds servers available to sync
# # rhui-manager cds sync
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help         show this help message and exit
# sync: sync content to specified cds
#     --cds_id - identifies the cds to sync (required)
# # rhui-manager cds clusters
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help  show this help message and exit
# clusters: list of cds clusters
# # rhui-manager cds repos
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help            show this help message and exit
# repos: list of repositories for provided cluster
#     --cluster_name - name of cluster (required)
# # rhui-manager client
# Red Hat client management
#     labels    : list the labels required for client certificate creation
#     cert      : create a content certificate for a rhui client
#     rpm       : create a client config rpm
# # rhui-manager client labels
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help  show this help message and exit
# labels: list the labels required for client certificate creation
# # rhui-manager client cert
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help            show this help message and exit
# cert: create a content certificate for a rhui client
#     --repo_label - identifies the repositories to add. Comma delimited string of repo labels (required)
#     --name - identifies the certificate name (required)
#     --days - number of days cert will be valid (required)
#     --dir - directory where the certificate will be stored (required)
# # rhui-manager client rpm
# Usage: rhui-manager [options]
# 
# Options:
#   -h, --help            show this help message and exit
# rpm: create a client config rpm
#     --private_key - entitlement private key  (required)
#     --entitlement_cert - entitlement certificate  (required)
#     --primary_cds - the cds used as the primary load balancer for a the cds cluster (required)
#     --ca_cert - full path to CA certificate (required)
#     --rpm_version - version number of the client config rpm (required)
#     --rpm_name - name of the client config rpm (required)
#     --dir - directory where the rpm will be created (required)
# [root@rhui-2 ~]#
#
set -e

list_subcmds_from_out () {
    test "x$@" = "x" || echo "$@" | sed -nr 's/\s+([^\s:]+):.*/\1/p'
}
list_subcmds_recur () {
    local sc=$@
    local help=$($sc --help)
    local scs=$(list_subcmds_from_out "$help")
    echo "# $sc"; echo "$help"
    for ssc in $scs; do list_subcmds_recur $sc $ssc; done
}

list_subcmds_recur ${@:-rhui-manager}

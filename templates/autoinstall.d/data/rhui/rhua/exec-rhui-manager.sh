#! /bin/bash
#
# Exec rhui-manager and run commands w/o any interactions.
#
# Author: Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# Limitations:
# - It's just echo-ing commands to rhui-manager and commands take some time to
#   get response may fail, eg. timeout 120 $0 r a 3 c y  # -> NG
# - You must run rhui-manager fist (configrue client entitlement cert and key)
#   before running this.
#
set -e

if test $# -eq 0; then
    cat << EOU
Usage: [timeout <timeout_sec>] $0 command_0 [command_1 [...]]
Examples:
  $0 r l  # List Repos
  $0 c l  # List CDSes
  timeout 10 $0 c i 1 c # Show the info of the first CDS cluster
  timeout 30 $0 n l  # List Entitlements
EOU
    exit 0
fi

if test -f /etc/pki/rhui/entitlement-ca.crt; then
    timeout 3 rhui-manager cert --help > /dev/null || \
    read -s -p 'RHUI Manager Password: ' -t 5 RHUI_MANAGER_PWD
else
    echo "You must initialize rhui-manager first!"
    exit 1
fi

function _exec_rhui_manager () {
    local cs=''
    test "x${RHUI_MANAGER_PWD}" = "x" && local rm_opt= || local rm_opt="--username admin --password ${RHUI_MANAGER_PWD}"
    for c in $@; do cs="${cs}$c\n"; done
    echo; sleep 2
    echo -ne "${cs}q\n" | rhui-manager ${rm_opt}; echo
}

_exec_rhui_manager $@

# vim:sw=4:ts=4:et:

#! /bin/bash
#
# Find the subscription pool ID by product name.
#
# (It may be similar to `subscription-manager list --available
# --matches=PRODUCT` although I cannot get expected results w/ it.)
#
# Author: Satoru SATOH <ssato at redhat.com>
# License: MIT
#
set -e

found_pools () {
    local prod="${1}"
    local input="${2:-$(subscription-manager list --available)}"

    sed -nr "
/^Subscription Name:/ {
    s/^.+: +([^[:blank:]]+.+)$/\1/
    h
}
/^ +${prod}$/ {
    s/^ +(${prod})$/\1/
    H
}
/^Pool ID:/ {
    s/^Pool ID: +([[:alnum:]]+)/\1/
    H
    x
    /.*${prod}.*/ { h; }
}
/^Available:/ {
    s/^Available: +([[:digit:]]+)/\1/
    H
    x
    /.*${prod}.*/ { x; }
}
/^Ends:/ {
    s/^Ends: +([^[:blank:]]+)/\1/
    H
    x
    /.*${prod}.*/ {
        s/^.*${prod}\n//
        s/\n/ /g
        # s/^/  /g
        p
    }
}
" $input | sort -r -k 2
}

PRODUCT="${1}"
INPUT=${2}

if test $# -eq 0 -o "$1" = "-h" -o "$1" = "--help"; then
    cat << EOH
Usage: ${0} PRODUCT [INPUT]
    where PRODUCT   Product name to find the pool ID of which subscription
                    contains the product. It may contain spaces in its name and
                    must be quoted if so.
          INPUT     Specify the output filepath of 'subscription-manager list
                    --available' if you run it before and have its output.

Examples:

    \$ ./sm-find-subpool-by-prod.sh "Red Hat Enterprise Linux Atomic Host"
    # Red Hat Enterprise Linux Atomic Host:
    8a8xx***********************xxxx 19141 01/01/2022
    8a8xx***********************xxxx 1 05/06/2015
    \$
EOH
    exit 0
fi

echo "# ${PRODUCT}:"
found_pools "${PRODUCT:?}" "${INPUT}"

# vim:sw=4:ts=4:et:

#! /bin/bash
#
# .. seealso:: RHUI 3.0 System Admin Guide, 6.1. Generate an RSA Key Pair: http://red.ht/2r8pkHh
#
set -ex

source ${0%/*}/config.sh

test -f ~/.ssh/id_rsa || ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

for cds in ${CDS_SERVERS:?}; do
    grep -E "^$cds" ~/.ssh/known_hosts || ssh-copy-id ${cds}
done

# vim:sw=4:ts=4:et:

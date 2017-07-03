#! /bin/bash
#
# Run some hammer * list commands
#
set -ex

LOGDIR=${1:-${0%/*}}
ORG_ID=$(cat ~/.hammer/organization_id.txt || echo "1")

hammer --csv product list --organization-id ${ORG_ID:?} | sort
hammer --csv repository-set list --organization-id ${ORG_ID} --product "Red Hat Enterprise Linux Server" | sort
hammer --csv subscription list --organization-id ${ORG_ID}
hammer --csv host-collection list --organization-id ${ORG_ID}
hammer --csv activation-key list --organization-id ${ORG_ID}

# vim:sw=2:ts=2:et:

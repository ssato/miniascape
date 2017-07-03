#! /bin/bash
#
# Run some hammer * list commands
#
set -ex

LOGDIR=${1:-${0%/*}}
ORG_ID=$(cat ~/.hammer/organization_id.txt || echo "1")

hammer --csv organization list
hammer --csv location list

items="
subscription product sync-plan host-collection lifecycle-environment
content-view activation-key
"

for item in ${items:?}; do hammer --csv ${item} list --organization-id ${ORG_ID:?} | sort; done

ORG_NAME=$(hammer --csv organization list | sed -nr "s/${ORG_ID},([^,]+),.*/\1/p")
ENABLED_PRODUCTS=$(hammer --csv product list --organization-id ${ORG_ID} | sed -nr "1d; s/^([[:digit:]]+),([^,]+),.*,${ORG_NAME},[^0][^,]*,.*/\1,\2/p")

cat << EOM
ORG_NAME: ${ORG_NAME:?}
Products (enabled): ${ENABLED_PRODUCTS:?}
EOM

for item in repository-set repository; do
    while read line; do
        test "x$line" = "x" || (
        prod_id=${line%%,*}
        hammer --csv ${item} list --organization-id ${ORG_ID} --product-id ${prod_id} | sort
        )
    done << EOC
${ENABLED_PRODUCTS}
EOC
done

# vim:sw=4:ts=4:et:

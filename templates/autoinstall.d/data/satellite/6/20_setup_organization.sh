#! /bin/bash
#
# Setup Satellite Ogranization as needed.
#
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
set -ex

# WORKDIR, ORG_NAME, ORG_LABEL
source ${0%/*}/config.sh

# Setup Hammer user config if not yet.
source ${WORKDIR}/setup_hammer_user_conf.sh

# Create Organization if not found.
hammer --csv organization list | grep -qE ",${ORG_LABEL}," 2>/dev/null || \
hammer organization create --name="${ORG_NAME}" --label="${ORG_LABEL}"
hammer --output=yaml organization list

# Create Location if not found.
hammer --csv location list | grep -qE ",${LOC_NAME}," 2>/dev/null || \
hammer location create --name="${LOC_NAME}"
hammer --output=yaml location list

org_id=$(hammer --output=yaml organization info --label "${ORG_LABEL}" | sed -nr "s/^Id: //p")
loc_id=$(hammer --output=yaml location info --name "${LOC_NAME}" | sed -nr "s/^Id: //p")
echo "[Info] Organization ID: '${org_id:?}', Location ID: '${loc_id:?}'"

test -f ${ORG_ID_FILE} || (
echo ${org_id} > ${ORG_ID_FILE:?}.t && mv ${ORG_ID_FILE}.t ${ORG_ID_FILE}
)

# see: Satellite 6.2 Hammer CLI Guide, 1.4. Setting a Default Organization:
# http://red.ht/2Dv8A2x
hammer defaults list
hammer defaults add --param-name organization_id --param-value ${org_id}
hammer defaults add --param-name location_id --param-value ${loc_id}
hammer defaults list

# Upload Satellite manifest
# .. note:: manifest.zip may be base64-encoded.
#
MANIFEST_ZIP_BASE64=$(ls -1t ${WORKDIR}/manifest*.zip.base64 | head -n 1)
MANIFEST_ZIP=${MANIFEST_ZIP_BASE64/.base64/}

test -f ${MANIFEST_ZIP:?} || \
(
test -f ${MANIFEST_ZIP_BASE64:?} &&
base64 -d ${MANIFEST_ZIP_BASE64:?} > ${MANIFEST_ZIP}
)
hammer subscription upload --file ${MANIFEST_ZIP}

# vim:sw=2:ts=2:et:
{#
#}

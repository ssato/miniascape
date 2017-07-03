#! /bin/bash
#
# Setup Satellite Ogranization as needed.
#
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
set -ex

# WORKDIR, ORG_NAME, ORG_LABEL, ORG_ID_FILE
source ${0%/*}/config.sh

# Setup Hammer user config if not yet.
source ${WORKDIR}/setup_hammer_user_conf.sh

# Create Organization if not found.
hammer --csv organization list | grep -qE ",${ORG_LABEL}," 2>/dev/null || \
hammer organization create --name="${ORG_NAME}" --label="${ORG_LABEL}"

test -f ${ORG_ID_FILE} || \
(
hammer --output=yaml organization info --label "${ORG_LABEL}" | sed -nr "s/^Id: //p" > ${ORG_ID_FILE:?}.t && \
mv ${ORG_ID_FILE}.t ${ORG_ID_FILE}
)

# Create Location if not found.
hammer --csv location list | grep -qE ",${LOC_NAME}$" 2>/dev/null || \
hammer location create --name="${LOC_NAME}"

# Upload Satellite manifest
# .. note:: manifest.zip may be base64-encoded.
#
MANIFEST_ZIP_BASE64=$(ls -1 ${WORKDIR}/manifest*.zip.base64 | head -n 1)
MANIFEST_ZIP=${MANIFEST_ZIP_BASE64/.base64/}

test -f ${MANIFEST_ZIP:?} || \
(
test -f ${MANIFEST_ZIP_BASE64:?} &&
base64 -d ${MANIFEST_ZIP_BASE64:?} > ${MANIFEST_ZIP}
)
hammer subscription upload --organization-id $(cat ${ORG_ID_FILE}) --file ${MANIFEST_ZIP}

# vim:sw=2:ts=2:et:
{#
#}

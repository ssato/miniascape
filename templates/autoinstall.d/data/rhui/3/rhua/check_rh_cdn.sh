#! /bin/bash
#
# A script to check it can access to RH CDN with using RHUI entitlement cert.
#
# Author: Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# Usage: $0 [TLS_CLI_CERT [TIMEOUT_SEC [RH_CDN_URL [CHECK_KEYWORD]]]]
#
set -ex

SELF_DIR=${0%/*}

TLS_CA_CERT=/etc/rhsm/ca/redhat-uep.pem
TLS_CLI_CERT=${1:-$(ls -t /etc/pki/rhui/redhat/*.pem | head -n 1)}
TIMEOUT=${2:-5}  # [sec]
MAX_TIMEOUT=60
RH_CDN_URL=${3:-https://cdn.redhat.com/content/dist/rhel/rhui/server/7/7Server/x86_64/os/repodata/repomd.xml}
CHECK_KEYWORD='200 OK'   # primary.xml, ...
CURL_PROXY_OPT=  # ex. --proxy https://proxy.example.com:8080 --proxy-user foo:********

test -f ${SELF_DIR:?}/config.sh && source ${SELF_DIR:?}/config.sh

#timeout ${TIMEOUT:?} \
#--connect-timeout ${TIMEOUT:?} --max-timeout ${MAX_TIMEOUT:?} \
curl -v ${CURL_PROXY_OPT} \
--connect-timeout ${TIMEOUT:?} \
--cacert ${TLS_CA_CERT:?} --cert ${TLS_CLI_CERT:?} ${RH_CDN_URL:?} 2>&1 | grep -q "${CHECK_KEYWORD:?}"

# vim:sw=4:ts=4:et:

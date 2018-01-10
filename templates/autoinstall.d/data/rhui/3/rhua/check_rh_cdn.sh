#! /bin/bash
#
# A script to check it can access to RH CDN with using RHUI entitlement cert.
#
# Author: Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# Usage: $0 [TLS_CLI_CERT [TIMEOUT_SEC [RH_CDN_URL]]]
#
# Example:
#
# [root@rhui-2 ~]# ./$0
# 
set -ex

TLS_CA_CERT=/etc/pki/rhui/ca.crt
TLS_CLI_CERT=${1:-$(ls -1 /etc/pki/rhui/redhat/*.pem | head -n 1)}
TIMEOUT=${2:-5}  # [sec]
RH_CDN_URL=${3:-https://cdn.redhat.com/content/dist/rhel/rhui/server/7/7Server/x86_64/os/repodata/repomd.xml}

timeout ${TIMEOUT:?} \
curl -v \
--cacert ${TLS_CA_CERT:?} \
--cert ${TLS_CLI_CERT:?} \
${RH_CDN_URL:?}

# vim:sw=4:ts=4:et:

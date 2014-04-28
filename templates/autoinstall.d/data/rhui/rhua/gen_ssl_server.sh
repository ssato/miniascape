#! /bin/bash
set -e

# SSL parameters:
COUNTRY=JP
STATE=Tokyo
ORGANIZATION=$1
SERVER_FQDN=$2
DAYS=${3:-3650}
KEY_BITS=${4:-2048}
SSL_CA_CRT=${5:-rhui-ca.crt}
SSL_CA_KEY=${6:-rhui-ca.key}

if test $# -lt 2; then
    echo "Usage: $0 ORGANIZATION SERVER_FQDN [DAYS [KEY_BITS [SSL_CA_CRT [SSL_CA_KEY]]]]"
    exit 0
fi

openssl genrsa -out ${SERVER_FQDN}.key ${KEY_BITS}
openssl req -new -key ${SERVER_FQDN}.key -subj "/C=${COUNTRY}/ST=${STATE}/O=${ORGANIZATION}/CN=${SERVER_FQDN}" -out ${SERVER_FQDN}.csr
openssl x509 -req -days ${DAYS} -CA ${SSL_CA_CRT} -CAkey ${SSL_CA_KEY} -in ${SERVER_FQDN}.csr -out ${SERVER_FQDN}.crt

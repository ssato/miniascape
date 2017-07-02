#! /bin/bash
#
# Setup hammer user configuration and check access
#
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
set -ex

SYS_ANSER_FILE=/etc/foreman-installer/scenarios.d/satellite-answers.yaml
HAMMER_SYS_CONF=/etc/hammer/cli.modules.d/foreman.yml

HAMMER_USER_CONF_DIR=${HOME}/.hammer/
HAMMER_USER_CONF=${HAMMER_USER_CONF_DIR:?}/cli_config.yml

test -f ${HAMMER_USER_CONF:?} || (

test -f ${HAMMER_SYS_CONF:?}
test -f ${SYS_ANSER_FILE:?}

# http://gsw-hammer.documentation.rocks/initial_configuration,_adding_red_repos/hammer_credentials.html
ADMIN_PASSWORD=$(shell sed -nr 's/^ *admin_password: ([^[:blank:]]+) *$/\1/p' ${SYS_ANSER_FILE})

test -d ${HAMMER_USER_CONF_DIR} || mkdir -p -m 0700 ${HAMMER_USER_CONF_DIR}

install -m 600 ${HAMMER_SYS_CONF} ${HAMMER_USER_CONF}
cat << EOF >> ${HAMMER_USER_CONF}
  :username: admin
  :password: ${HAMMER_ADMIN_PASSWORD}
EOF

# Test hammer works w/o password authentication.
hammer ping
hammer --output=yaml organization list
)

# vim:sw=2:ts=2:et:

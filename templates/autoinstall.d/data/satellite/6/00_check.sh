#! /bin/bash
#
# Various checks before Satellite installation.
#
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
# References:
# - Satellite 6.3 Installation Guide, 2. Preparing your environment for installation
#
set -ex

# SATELLITE_HOSTNAME
source ${0%/*}/config.sh

# Common checks
bash -x ${0%/*}/check.sh

timeout 5 hostname -f
date   # TODO: How to check if the time is correct?
df -h  # TODO: How to check if there is enough space to hold repos' data?

# vim:sw=2:ts=2:et:
{#
#}

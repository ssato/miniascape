#! /bin/bash
set -ex

ipa-server-install -a redhat -p redhat --hostname=$(hostname -f) -r m2.local

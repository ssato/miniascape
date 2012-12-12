#! /bin/bash
set -ex

ipa-server-install -a {{ ipa.admin.password }} -p {{ ipa.admin.password }} -r {{ domain }} --hostname=$(hostname -f) -U

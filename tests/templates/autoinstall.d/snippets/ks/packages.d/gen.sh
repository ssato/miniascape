#! /bin/sh
set -e
cd ${0%/*}
cat ../../../../../../templates/autoinstall.d/data/rhel_basic_tools_rpms \
    ../../../../../../templates/autoinstall.d/data/rhel_uninstalled_rpms \
> 00_out.exp
cat << EOF > 10_out.exp
@core
bash-completion
EOF
cat ../../../../../../templates/autoinstall.d/data/rhel_uninstalled_rpms \
>> 10_out.exp

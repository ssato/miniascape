#! /bin/bash
# vim:sw=4:ts=4:et:
# Create LIO-file based iSCSI LUNs with using targetcli
#
targetcli --help 2>/dev/null >/dev/null; rc=$?
if test $rc -ne 0; then
    echo "[Error] targetcli looks not found. Aborting..."
    exit 1
fi

set -e

# Example:
#targetcli /backstores/fileio create iscsi-shared-0 /var/lib/libvirt/images/iscsi-shared-0.img 1G
#targetcli /iscsi create iqn.2003-01.org.linux-iscsi.localhost.x8664:sn.a8c6dd6de931
#targetcli /iscsi/iqn.2003-01.org.linux-iscsi.localhost.x8664:sn.a8c6dd6de931/tpg1/luns create /backstores/fileio/iscsi-shared-0
#targetcli /iscsi/iqn.2003-01.org.linux-iscsi.localhost.x8664:sn.a8c6dd6de931/tpg1/portals create 192.168.155.254

{% for target in iscsi.targets %}targetcli /backstores/fileio create {{ target.name }} {{ target.path }} {{ target.size }}
targetcli /iscsi create {{ target.iqn }}
targetcli /iscsi/{{ target.iqn }}/tpg1/luns create /backstores/fileio/{{ target.name }}
targetcli /iscsi/{{ target.iqn }}/tpg1/portals create {% if target.ip is defined %}{{ target.ip }}{% else %}{{ gateway }}{% endif %}
{% endfor %}

# iptables:
echo "Check to see needed port is open and if not: "
echo "    run 'iptables -I INPUT -m tcp -p tcp --dport 3260 -j ACCEPT'"

#! /bin/bash
set -e

netconfdir=${0%/*}
{% for net in networks %}
if `virsh net-list --all | grep -q $net 2>/dev/null`; then
    echo "Network $net already exists. Nothing to do..."
else
    netxml=${netconfdir:?}/${net}.xml
    if test -f ${netxml}; then
        virsh net-define ${netxml} && virsh net-start ${net} && virsh net-autostart ${net}
    else
        echo "[Error] network xml ${netxml} does not exist!"
    fi
fi
{% endfor %}

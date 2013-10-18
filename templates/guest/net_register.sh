#! /bin/bash
# see also `[...]/usr/libexec/miniascape/guest_network_register.sh -h`
#

# Use installed version of 'guest_network_register.sh' if exists:
register_sh=/usr/libexec/miniascape/guest_network_register.sh
test -x ${register_sh} || register_sh=${0%/*}/../../host/${register_sh}

{% for nic in interfaces -%}
{%     if nic.mac is defined and nic.ip is defined and nic.fqdn is defined -%}
bash {{ script }} -m {{ nic.mac }} -n {{ nic.network|default('default') }} {{ nic.fqdn }} {{ nic.ip }}
{%-    endif %}
{% endfor %}


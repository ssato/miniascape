#! /bin/bash
#
# Update some pulp and rhu-rhui-tools configuration files
# just after RHUI rpms installed.
#
set -e
set -x

sed -i.save \
  -e 's/localhost.localdomain/{{ fqdn }}/' \
  -e 's,https://localhost,https://{{ fqdn }},g' \
  -e 's,http://localhost,http://{{ fqdn }},g' \
  /etc/pulp/consumer/consumer.conf

sed -i.save \
  -e 's/^server_name: localhost/server_name: {{ fqdn }}/' \
  -e 's,tcp://localhost:,tcp://{{ fqdn }}:,' \
  /etc/pulp/pulp.conf

{% if proxy is defined %}sed -i.save \
  -e 's/localhost/{{ fqdn }}/' -e "/^# proxy_pass:/ a \
proxy_url = https://{{ proxy.fqdn }}/\nproxy_port = {{ proxy_port }}" /etc/rhui/rhui-tools.conf
{% else %}
sed -i.save -e 's/localhost/{{ fqdn }}/' /etc/rhui/rhui-tools.conf
{% endif %}

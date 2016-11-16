#! /usr/bin/puppet apply
#
# It does several things to setup RHUI on RHUA.
#
# Prerequisites:
# - rhui-installer was installed from RHUI ISO image
# - CDSes and LBs (HA Proxy nodes) are ready and accessible with ssh from RHUA w/o password
# - Gluster FS was setup in CDSes and ready to access from RHUA
#

$rhui_installer_stamp_dir = "/root/setup/rhui-installer.d"
$rhui_installer_common_options = "{{ '-v' if rhui.rhui_installer.verbose }} {{ '--cds-lb-hostname %s' % rhui.lb.hostname }} {{ '--certs-country %s' % rhui.certs.country|default('JP') }} {{ '--certs-state %s' % rhui.certs.state|default('Tokyo') }} {{ '--certs-city %s' % rhui.certs.city|default('Shibuya-ku') }} {{ '--certs-org %s' % rhui.certs.org }} {{ '--certs-org-unit %s' % rhui.certs.unit|default('Unit') }} {{ rhui.rhui_installer.extra_options|default('') }}"


file { "${rhui_installer_stamp_dir}":
    ensure => directory,
}

# puppet should be ready to use on RHUA if it's true.
package { "rhui-installer":
    ensure => installed,
}

{% for fs in rhui.remote_fs if fs.server and fs.path -%}
$remote_fs_{{ loop.index }}_stamp="${rhui_installer_stamp_dir}/{{ fs.server }}.stamp"

exec { "run rhui-installer for {{ server }}":
    command => "rhui-installer ${rhui_installer_common_options} --remote-fs-type={{ fs.type|default('glusterfs') }} --remote-fs-server={{ fs.server }}:{{ fs.path }}",
    creates => $remote_fs_{{ loop.index }}_stamp,
    unless => "test -f ${remote_fs_{{ loop.index }}_stamp}",
}
{% endfor %}

{% for cds in rhui.cdses -%}
exec { "Add CDS: {{ cds }}":
    command => "rhui cds add {{ cds }} root /root/.ssh/id_rsa -u",
    unless => "rhui cds list -m | grep -E 'hostname.: .{{ cds }}'",
}
{% endfor %}

{% for lb in rhui.lb.servers -%}
exec { "Add Load Balancer: {{ lb }}":
    command => "rhui haproxy add {{ lb }} root /root/.ssh/id_rsa -u",
    unless => "rhui haproxy list -m | grep -E 'hostname.: .{{ lb }}'",
}
{% endfor %}

# vim:sw=4:ts=4:et:

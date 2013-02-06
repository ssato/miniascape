#! /bin/bash
# see also virt-install(1)
#
{%- macro net_option(nic) -%}
network={{ nic.network|default('network') }},model={{ nic.model|default('virtio') }},mac={{ nic.mac|default('RANDOM') }}
{%- endmacro -%}
{%- macro disk_option(disk, create=true) -%}
{%-     if disk.pool is defined -%}
{%-         if disk.vol is defined %}vol={{ disk.pool }}/{{ disk.vol }}{% else %}pool={{ disk.pool }}{% endif -%}
{%-     else %}path={{ disk.path }}
{%-     endif -%}
,format={{ disk.format|default('qcow2') }},cache={{ disk.cache|default('none') }}
{%-     if create %},size={{ disk.size|default('5') }}{% endif -%}{# use pre-built volume if not 'create' flag is set. #}
{%-     if disk.perms is defined %},perms={{ disk.perms }}{% endif -%}
{%-     if disk.bus is defined %},bus={{ disk.bus }}{% endif -%}
{%-     if disk.format == 'raw' and disk.sparse is defined %},sparse={{ disk.sparse }}{% endif -%}
{%- endmacro %}
set -ex
{% block kscfg %}test $# -gt 0 && ks_path=$1 || ks_path=${0%/*}/ks.cfg
kscfg=${ks_path##*/}{% endblock %}
{% block location %}location={{ virtinst.location }}{% endblock %}

{% block virtinst_disks_hack %}{% if disks|length >= 2 %}
virtinst_ver_s=`virt-install --version 2>/dev/null`
virtinst_ver=${${virtinst_ver_s#*.}%.*}
virtinst_rel=${virtinst_ver_s##*.}
need_disks_hack=$( (test ${virtinst_ver} -lt 600 || test ${virtinst_ver} -eq 600 && test ${virtinst_rel} -lt 3) && echo "true" || echo "false")
if test $need_disks_hack = "true"; then
  # Create storage volumes by virsh or qemu instead of virt-install as needed.
  # see also: rhbz#857424
{%     for disk in disks %}{% if not loop.first -%}
{%-         if disk.path is defined -%}
  test -f {{ disk.path }} || \
    {% if disk.format == 'raw' and disk.sparse != 'true' %}dd if=/dev/zero of={{ disk.path }} bs=1G count={{ disk.size|default('5') }}{% else %}qemu-img create -f {{ disk.format|default('qcow2') }} {{ disk.path }} {{ disk.size|default('5') }}{% endif %}
{%-         else -%}
      virsh vol-key {{ disk.vol }} {{ disk.pool|default('default') }} || \
      virsh vol-create-as {{ disk.pool|default('default') }} {{ disk.vol }} {{ disk.size|default('5') }}GiB --format {{ disk.format|default('qcow2') }}
{%-         endif -%}
{%-    endif %}{% endfor %}
  disk_options="{% for disk in disks %}{% if loop.first %}--disk {{ disk_option(disk) }} {% else %}--disk {{ disk_option(disk, false) }} {% endif %}{% endfor %}"
else
  disk_options="{% for disk in disks %}--disk {{ disk_option(disk) }} {% endfor %}"
fi{% else %}disk_options="{% for disk in disks %} --disk {{ disk_option(disk) }}{% endfor %}"{% endif %}{% endblock %}

virt-install \
{{ virtinst.basic_options }} \
--name={% if name is defined %}{{ name }}{% else %}{{ hostname }}{% endif %} \
--connect={{ virtinst.connect }} \
--wait={{ virtinst.waittime }} \
--ram={{ virtinst.ram }} \
--arch={{ virtinst.arch }} \
--vcpus={{ virtinst.vcpus }} {% if virtinst.cpu is defined %}--cpu {{ virtinst.cpu }}{% endif %} \
--graphics {{ virtinst.graphics }} \
--os-type={{ virtinst.os_type }} \
--os-variant={{ virtinst.os_variant }} \
{% if virtinst.cdrom %}--cdrom {{ virtinst.cdrom }}{% if virtinst.extra_args is defined and false %} --extra-args="{{ virtinst.extra_args }}"{% endif %}{% else %}--location=${location} --initrd-inject=${ks_path} --extra-args="ks=file:/${kscfg} ksdevice={{ ksdevice|default('eth0') }} {{ virtinst.extra_args|default('') }}"{% endif %} \
${disk_options} \
{% for nic in interfaces %}--network {{ net_option(nic) }} {% endfor %}


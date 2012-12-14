#! /bin/bash
# see also virt-install(1)
#
set -ex
test $# -gt 0 && ks_path=$1 || ks_path=${0%/*}/ks.cfg
kscfg=${ks_path##*/}
location={{ virtinst.location }}

# Create storage volumes by virsh or qemu instead of virt-install as needed.
# see also: rhbz#857424
{%     for disk in disks %}{% if not loop.first -%}
{%-         if disk.path is defined -%}
test -f {{ disk.path }} || \
    qemu-img create -f {{ disk.format|default('qcow2') }} {{ disk.path }} {{ disk.size|default('5') }}
{%-         else -%}
virsh vol-key {{ disk.vol }} {{ disk.pool|default('default') }} || \
    virsh vol-create-as {{ disk.pool|default('default') }} {{ disk.vol }} {{ disk.size|default('5') }}GiB --format {{ disk.format|default('qcow2') }}
{%-         endif -%}
{%-    endif %}{% endfor %}
{%- macro net_option(nic) -%}
network={{ nic.network|default('network') }},model={{ nic.model|default('virtio') }},mac={{ nic.mac|default('RANDOM') }}
{%- endmacro -%}
{%- macro disk_option(disk, first=true) -%}
{%-     if disk.pool is defined -%}
{%-         if disk.vol is defined %}vol={{ disk.pool }}/{{ disk.vol }}{% else %}pool={{ disk.pool }}{% endif -%}
{%-     else %}path={{ disk.path }}
{%-     endif -%}
,format={{ disk.format|default('qcow2') }},cache={{ disk.cache|default('none') }}
{%-     if first %},size={{ disk.size|default('5') }}{% endif -%}{# use pre-built volume if not first disk #}
{%-     if disk.perms is defined %},perms={{ disk.perms }}{% endif -%}
{%-     if disk.bus is defined %},bus={{ disk.bus }}{% endif -%}
{%- endmacro %}

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
{% for disk in disks %}{% if loop.first %}--disk {{ disk_option(disk) }} {% else %}--disk {{ disk_option(disk, false) }} {% endif %}{% endfor %} \
{% for nic in interfaces %}--network {{ net_option(nic) }} {% endfor %}

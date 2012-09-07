#! /bin/bash
# see also virt-install(1)
#
set -ex
test $# -gt 0 && ks_path=$1 || ks_path=${0%/*}/ks.cfg
kscfg=${ks_path##*/}

{%- macro net_option(nic) -%}
network={{ nic.network|default('network') }},model={{ nic.model|default('virtio') }},mac={{ nic.mac|default('RANDOM') }}
{%- endmacro -%}
{% macro disk_option(disk) -%}
{{ disk.type|default('pool') }}={{ disk.src|default('default') }},format={{ disk.format|default('qcow2') }},cache={{ disk.cache|default('none') }},size={{ disk.size|default('5') }}{% if disk.perms is defined %},perms={{ disk.perms }}{% endif %}
{%- endmacro %}

virt-install \
{{ virtinst.basic_options }} \
--name={% if name is defined %}{{ name }}{% else %}{{ hostname }}{% endif %} \
--connect={{ virtinst.connect }} \
--wait={{ virtinst.waittime }} \
--ram={{ virtinst.ram }} \
--arch={{ virtinst.arch }} \
--vcpus={{ virtinst.vcpus }} \
--graphics {{ virtinst.graphics }} \
--os-type={{ virtinst.os_type }} \
--os-variant={{ virtinst.os_variant }} \
--location={{ virtinst.location }} \
--initrd-inject=${ks_path} \
{% for disk in disks %}--disk "{{ disk_option(disk) }}" {% endfor %} \
{% for nic in interfaces %}--network "{{ net_option(nic) }}" {% endfor %} \
--extra-args="ks=file:/${kscfg} ksdevice={{ ksdevice|default('eth0') }} {{ virtinst.extra_args|default('') }}"

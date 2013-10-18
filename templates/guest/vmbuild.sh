#! /bin/bash
# see also virt-install(1)
#
{% macro net_option(nic) -%}
network={{ nic.network|default('network') }},model={{ nic.model|default('virtio') }},mac={{ nic.mac|default('RANDOM') }}
{%- endmacro -%}
{% macro disk_option(disk, create=true) -%}
{%     if disk.pool is defined -%}
{%         if disk.vol is defined -%}
vol={{ disk.pool }}/{{ disk.vol }}
{%-        else -%}
pool={{ disk.pool }}
{%-        endif -%}
{%     else -%}
path={{ disk.path }}
{%     endif -%}
,format={{ disk.format|default('qcow2') }},cache={{ disk.cache|default('none') }}
{#-    use pre-built volume if not 'create' flag is set. -#}
{%     if create -%}
,size={{ disk.size|default('5') }}
{%-    endif -%}
{%     if disk.bus is defined -%}
,bus={{ disk.bus }}
{%-    endif -%}
{%     if disk.perms is defined -%}
,perms={{ disk.perms }}
{%-    endif -%}
{%     if disk.format == 'raw' and disk.sparse is defined -%}
,sparse={% if disk.sparse %}true{% else %}false{% endif -%}
{%     endif -%}
{% endmacro -%}
set -ex
{% block kscfg -%}
test $# -gt 0 && ks_path=$1 || ks_path=${0%/*}/ks.cfg
kscfg=${ks_path##*/}
{%- endblock %}
name={% if name_prefix is defined %}{{ name_prefix }}{% endif -%}
{%  if hostname is defined %}{{ hostname }}{% else %}{{ name }}{% endif %}

{% block location -%}
{% if virtinst.cdrom -%}
{%     if virtinst.extra_args is defined and virtinst.extra_args -%}
# --extra-args="{{ virtinst.extra_args }}"  # It does not work w/ --cdrom but ...
{%     endif -%}
location_opts="--cdrom {{ virtinst.cdrom }}"
{% else -%}
location_opts="--location={{ virtinst.location }} --initrd-inject=${ks_path}"
ksdevice={{ ksdevice|default('eth0') }}
more_extra_args={{ virtinst.extra_args|default('') }}
{% endif -%}
{%- endblock %}

# Use virtio-scsi if available and there is a scsi disk:
virtio_scsi_controller=
{%- for disk in disks if disk.bus is defined and disk.bus == 'scsi' -%}
"--controller type=scsi,model=virtio-scsi"{% else %}""
{%- endfor %}

virt-install \
{{ virtinst.basic_options }} \
--name=${name:?} \
--connect={{ virtinst.connect }} \
--wait={{ virtinst.waittime }} \
--ram={{ virtinst.ram }} \
--arch={{ virtinst.arch }} \
--vcpus={{ virtinst.vcpus }} {% if virtinst.cpu is defined %}--cpu {{ virtinst.cpu }}{% endif %} \
--graphics {{ virtinst.graphics }} \
--os-type={{ virtinst.os_type }} \
--os-variant={{ virtinst.os_variant }} \
${virtio_scsi_controller} \
${location_opts} {% if virtinst.cdrom is not defined %}--extra-args="ks=file:/${kscfg} ksdevice=${ksdevice} ${more_extra_args}"{% endif %} \
{% for disk in disks -%}
--disk {{ disk_option(disk) }} \
{% endfor %} \
{% for nic in interfaces -%}
--network {{ net_option(nic) }} \
{% endfor %}


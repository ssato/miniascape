#! /bin/bash
# see also virt-install(1)
#
function genmac () { python -c 'from random import randint as f; print ":".join("%02x" % x for x in (0x52, 0x54, 0x00, f(0x00, 0x7f), f(0x00, 0xff),  f(0x00, 0xff)))'; }
{% macro net_option(nic) -%}
{%     if nic.bridge is defined -%}
bridge={{ nic.bridge }}
{%-    else -%}
network={{ nic.network|default('default') }}
{%-    endif -%}
,model={{ nic.model|default('virtio') }},mac={% if nic.mac is defined and nic.mac != 'RANDOM' %}{{ nic.mac }}{% else %}$(genmac){% endif %}
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
{%-    endif -%}
{%     if disk.format is defined and disk.format != 'none' -%}
,format={{ disk.format|default('qcow2') }},cache={{ disk.cache|default('none') }}
{%-    endif -%}
{#-    use pre-built volume if not 'create' flag is set. -#}
{%     if disk.size is defined and disk.size > 0 -%}
{%         if create -%}
,size={{ disk.size }}
{%-        endif -%}
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
connect=${QEMU_CONNECT:-{{ virtinst.connect }}}

{% block location -%}
{% if virtinst.cdrom -%}
{%     if virtinst.extra_args is defined and virtinst.extra_args -%}
# --extra-args="{{ virtinst.extra_args }}"  # It does not work w/ --cdrom but ...
{%     endif -%}
location_opts="--cdrom {{ virtinst.cdrom }}"
{% else -%}
location_opts="--location={{ virtinst.location }} --initrd-inject=${ks_path}"
more_extra_args="{{ virtinst.extra_args|default('') }}"
{%     if interfaces|length > 1 -%}
more_extra_args="$more_extra_args ksdevice={{ ksdevice|default('eth0') }}"
{%     endif -%}
{% endif -%}
{%- endblock %}

{% block virtio_scsi_def -%}
# Use virtio-scsi if available and there is a scsi disk:
virtio_scsi_controller=
{%-     for disk in disks if disk.bus is defined and disk.bus == 'scsi' -%}
{%-         if loop.first -%}
"--controller=scsi,model=virtio-scsi"{% else %}""
{%-         endif -%}
{%-     endfor %}
{%- endblock %}

{% block virt_install -%}
virt-install \
{{ virtinst.basic_options }} \
--name=${name:?} \
--connect=${connect:?} \
--wait={{ virtinst.waittime }} \
--ram={{ virtinst.ram }} \
--arch={{ virtinst.arch }} \
--vcpus={{ virtinst.vcpus }} {% if virtinst.cpu is defined %}--cpu {{ virtinst.cpu }}{% endif %} \
--graphics {{ virtinst.graphics }}{% if keyboard is defined %},keymap={{ keyboard }}{% endif %} \
--os-type={{ virtinst.os_type }} \
--os-variant={{ virtinst.os_variant }} \
{%	if virtinst.os_variant == 'rhel7' -%}
--console pty,target_type=serial \
{%	endif -%}
${virtio_scsi_controller} \
${location_opts} {% if virtinst.cdrom is not defined %}--extra-args="ks=file:/${kscfg} ${more_extra_args}"{% endif %} \
{%    for disk in disks -%}
--disk {{ disk_option(disk) }} \
{%    endfor %} \
{%    for nic in interfaces -%}
--network {{ net_option(nic) }} \
{%    endfor %}
{%- endblock %}

#! /bin/bash
# see also virt-install(1)
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
{%     if disk.shareable is defined and disk.shareable -%}
,shareable=on
{%-    endif -%}
{%     if disk.format == 'raw' and disk.sparse is defined -%}
,sparse={% if disk.sparse %}yes{% else %}no{% endif -%}
{%     endif -%}
{% endmacro -%}
set -ex
test $# -gt 0 && ks_path=$1 || ks_path=${0%/*}/ks.cfg
kscfg=${ks_path##*/}
name={{ '%s' % name_prefix if name_prefix }}{{ '%s' % hostname or name }}
connect=${QEMU_CONNECT:-{{ virtinst.connect|default('qemu:///system') }}}
{% block location -%}
{%     if virtinst.cdrom -%}
location_opts="--cdrom {{ virtinst.cdrom }}"
{%     else -%}
location_opts="--location={{ virtinst.location }} --initrd-inject=${ks_path}"
extra_args="{{ 'inst.loglevel=debug inst.headless inst.text inst.' if virtinst.os_variant and virtinst.os_variant == 'rhel7' }}ks=file:/${kscfg} {{ virtinst.extra_args|default('') }}"
{%         if interfaces|length > 1 -%}
extra_args="$extra_args{{ ' ksdevice=%s' % ksdevice if ksdevice and not (virtinst and virtinst.os_variant in ('rhel7', 'fedora21')) }}"
{%         endif -%}
{%     endif -%}
{% endblock %}

{% block create_vols -%}
{%     for disk in disks if disk.pool and disk.vol -%}
{{ '# create storage volumes on ahead of virt-install run.' if loop.first }}
virsh vol-key {{ disk.vol }} {{ disk.pool }} || \
virsh vol-create-as {{ disk.pool }} {{ disk.vol }} {{ disk.size }}GiB --format {{ disk.format|default("qcow2") }}
{%     endfor %}
{% endblock %}

{% block virtio_scsi_def -%}
# Use virtio-scsi if available and there is a scsi disk:
{%     for disk in disks if disk.bus and disk.bus == 'scsi' -%}
{{ 'virtio_scsi_controller="--controller=scsi,model=virtio-scsi"' if loop.first -}}
{%     endfor -%}
{% endblock %}

{% block virt_install -%}
virt-install \
{{     virtinst.basic_options|default('--check-cpu --hvm --accelerate --noautoconsole') }} \
--name=${name:?} \
--connect=${connect:?} \
--wait={{ virtinst.waittime|default('10') }} \
--ram={{ virtinst.ram|default('1024') }} \
--arch={{ virtinst.arch|default('x86_24') }} \
--vcpus={{ virtinst.vcpus }} \
{{     ' --cpu %s' % virtinst.cpu if virtinst.cpu }} \
--graphics {{ virtinst.graphics|default('vnc') -}}
{{-    ',keymap=%s' % virtinst.keyboard if virtinst.keyboard else keyboard|default('us') }} \
--os-type={{ virtinst.os_type|default('linux') }} \
--os-variant={{ virtinst.os_variant }} \
{%     if use_serial_console and virtinst.os_variant and virtinst.os_variant == 'rhel7' -%}
--console pty,target_type=serial {%	endif -%} \
${virtio_scsi_controller} \
${location_opts} \
--extra-args="${extra_args}" \
{%     for disk in disks -%}
--disk {{ disk_option(disk) }} \
{%     endfor %} \
{%     for nic in interfaces -%}
--network {{ net_option(nic) }} \
{%     endfor %}
{% endblock %}
# vim:sw=4:ts=4:et:

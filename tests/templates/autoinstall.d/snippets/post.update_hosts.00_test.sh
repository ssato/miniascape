#! /bin/bash
set -e

curdir=${0%/*}
ctxfile=${curdir}/etc/hosts.ctx.yml
sh_output=${curdir}/etc/post.update_hosts.sh
tmpl=${curdir}/../../../../templates/autoinstall.d/snippets/post.update_hosts

# setup
mkdir -p ${curdir}/etc
cat << EOF > ${curdir}/etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
EOF

cat << EOF > ${ctxfile}
ip: 192.168.100.1
fqdn: foo.example.com
hostname: foo

hosts:
  - ip: 192.168.100.100
    fqdn: bar.example.com
    host: bar
  - ip: 192.168.100.101
    fqdn: baz.example.com
  - ip: 192.168.100.102
    host: hoge
  - ip: 192.168.100.1
    host: foo-cname
  - host: no_ip_host
EOF

jinja2-cli render -C ${ctxfile} -o ${sh_output} ${tmpl}


#! /bin/bash
set -x
logdir=/root/setup/logs
logfile=${logdir}/check.sh.log.$(date +%F_%T)
test -d ${logdir:?} || mkdir -p ${logdir}
(
cat /etc/redhat-release
uname -a
hostname; hostname -s; hostname -f || :
date
which chronyc && \
(systemctl status chronyd && systemctl is-enabled chronyd && chronyc sources) || \
(which ntpq && systemctl status ntpd && systemctl is-enabled ntpd && ntptime)
/sbin/ip a
/sbin/ip r
df -h
mount
cat /etc/fstab
pvscan; vgscan; lvscan
which gendiff && gendiff /etc .save || :
for f in /etc/sysconfig/network-scripts/{ifcfg-*,route*}; do
    echo "# ${f##*/}:"
    cat $f
done
ls -l /etc/sysctl.d; sysctl -a > ${logdir}/sysctl-a.txt
ls -l /etc/sudoers.d
rpm -qa --qf "%{n},%{v},%{r},%{arch},%{e}\n" | sort > ${logdir}/rpm-qa.0.txt
svcs="{{ services.enabled|join(' ')|default('sshd') }}"
test -d /etc/systemd && (systemctl; systemctl list-unit-files; for s in $svcs; do systemctl status $s; done) || \
(/sbin/chkconfig --list; for s in $svcs; do service $s status; done)
) 2>&1 | tee ${logfile}

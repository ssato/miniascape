#! /bin/bash
set -x
logdir=/root/setup/logs
test -d ${logdir:?} || mkdir -p ${logdir}
(
cat /etc/redhat-release
uname -a
/sbin/ip a
/sbin/ip r
df -h
mount
gendiff /etc .save
for f in /etc/sysconfig/network-scripts/ifcfg-*; do
    echo "# ${f##*/}:"
    cat $f
done
ls -l /etc/sysctl.d; sysctl -a > ${logdir}/sysctl-a.txt
ls -l /etc/sudoers.d
rpm -qa --qf "%{n},%{v},%{r},%{arch},%{e}\n" | sort > ${logdir}/rpm-qa.0.txt
test -d /etc/systemd && (systemctl; systemctl list-unit-files) || \
    /sbin/chkconfig --list
) 2>&1 | tee ${logdir}/check.sh.log

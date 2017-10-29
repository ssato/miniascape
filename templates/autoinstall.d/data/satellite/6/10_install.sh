#! /bin/bash
#
# Install Satellite 6.x
#    - Satellite RPM Installation: ./install_packages in Satellite ISO image
#    - Satellite Installation: satellite-installer
#
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#
# Prerequisites:
# - RHEL and Satellite 6.x ISO images
#
# References:
# - Satellite 6.2 Installation Guide, 2. Preparing your environment for installation
# - Satellite 6.2 Installation Guide, 3.2. Downloading and Installing from a Disconnected Network
# - 
set -ex

# SATELLITE_INSTALLER_OPTIONS, LOGDIR, USE_RPM_INSTALL_SCRIPT, RHEL_ISO,
# SATELLITE_ISO
source ${0%/*}/config.sh

rpm -q katello || (

test "x${USE_RPM_INSTALL_SCRIPT:?}" = "yes" && (
trap "umount /mnt" INT TERM && \
mount -o ro,loop ${SATELLITE_ISO:?} /mnt && cd /mnt && ./install_packages; \
cd - && umount /mnt
#alternatives --set java java-1.7.0-openjdk.x86_64  # @see https://bugzilla.redhat.com/show_bug.cgi?id=1418410
) || (
MNT_DIR=/var/www/html
RHEL_SUBDIR=pub/rhel-7/
SATELLITE_SUBDIR=pub/satellite-6/
BASE_URL_PREFIX=file://${MNT_DIR:?}

test -f ${RHEL_ISO:?}
test -f ${SATELLITE_ISO:?}

# RHEL
f=/etc/yum.repos.d/rhel-7.x-iso.repo
test -f $f || \
cat << EOF > /etc/yum.repos.d/rhel-7.x-iso.repo
[rhel-7.x]
name=RHEL 7.x
baseurl=${BASE_URL_PREFIX:?}/${RHEL_SUBDIR}/
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
gpgcheck=1
enabled=1
EOF

test -d ${MNT_DIR}/${RHEL_SUBDIR}/Packages || (
mkdir -p ${MNT_DIR}/${RHEL_SUBDIR}
mount -o ro,loop ${RHEL_ISO:?} ${MNT_DIR}/${RHEL_SUBDIR}
)

# RH Satellite
f=/etc/yum.repos.d/rhs-6.x-iso.repo
test -f $f || \
cat << EOF > /etc/yum.repos.d/rhs-6.x-iso.repo
[rhs-3.x]
name=RH Satellite 6.x
baseurl=${BASE_URL_PREFIX:?}/${SATELLITE_SUBDIR}/
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
gpgcheck=1
enabled=1

[rhscl]
name=RHEL Software Collection
baseurl=${BASE_URL_PREFIX:?}/${SATELLITE_SUBDIR}/RHSCL/
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
gpgcheck=1
enabled=1
EOF
test -d ${MNT_DIR}/${SATELLITE_SUBDIR}/Packages || (
mkdir -p ${MNT_DIR}/${SATELLITE_SUBDIR}
mount -o ro,loop ${SATELLITE_ISO:?} ${MNT_DIR}/${SATELLITE_SUBDIR}
)

yum install --disablerepo='*' --enablerepo=rhel-7.x --enablerepo=rhs-3.x --enablerepo=rhscl -y satellite
)
)

f=${LOGDIR}/satellite-installer.stamp
test -f ${f} || (
test -d ${LOGDIR:?} || mkdir -p ${LOGDIR}
satellite-installer --scenario satellite \
  ${SATELLITE_INSTALLER_OPTIONS:?} | \
		tee 2>&1 ${LOGDIR}/satellite-installer.$(date +%F_%T).log && touch $f
)

# vim:sw=2:ts=2:et:
{#
#}

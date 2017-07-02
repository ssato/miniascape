#! /bin/bash
#
# Install Satellite 6.x
#    - Satellite RPM Installation: ./install_packages in Satellite ISO image
#    - Satellite Installation: satellite-installer
#
# Author: Satoru SATOH <ssato/redhat.com>
# License: MIT
#

# References:
# - Satellite 6.2 Installation Guide, 2. Preparing your environment for installation
# - Satellite 6.2 Installation Guide, 3.2. Downloading and Installing from a Disconnected Network
# - 
set -ex

# KATELLO_INSTALLER_OPTIONS, LOGDIR
source ${0%/*}/config.sh

rpm -q katello || (

SATELLITE_ISO=$(ls -1 ${SATELLITE_ISO_DIR}/satellite*.iso | head -n 1)
test -f ${SATELLITE_ISO}

# Install Satellite RPMs
trap "umount /mnt" INT TERM && \
mount -o ro,loop ${SATELLITE_ISO:?} /mnt && cd /mnt && ./install_packages; \
cd - && umount /mnt

#alternatives --set java java-1.7.0-openjdk.x86_64  # @see https://bugzilla.redhat.com/show_bug.cgi?id=1418410

test -d ${LOGDIR:?} || mkdir -p ${LOGDIR}

satellite-installer --scenario satellite \
  ${SATELLITE_INSTALLER_OPTIONS:?} | \
		tee 2>&1 ${LOGDIR}/satellite-installer.$(date +%F_%T).log
)

# vim:sw=2:ts=2:et:

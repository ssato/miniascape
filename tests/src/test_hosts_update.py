import nose
import os
import shutil

from nose.tools import with_setup, assert_raises
from globals import *

import hosts_update



WORKDIR = None
AUG = None

IP_00 = '127.0.0.1'  # Must exists in /etc/hosts.
FQDN_0 = 'test-1.example.com'
HOST_0 = 'test-1'

# "300.0.0.1" is invalid IP address for hosts and must not exist in /etc/hosts.
# Because it's invalid, it should be suitable for testing purpose.
IP_0 = '300.0.0.1'
IP_1 = '300.0.0.2'



def setup():
    global WORKDIR, AUG, BUILD_SRCDIR

    WORKDIR = setupdir()
    print "BUILD_SRCDIR = " + BUILD_SRCDIR
    print "BUILD_DATADIR = " + BUILD_DATADIR
    etcdir = os.path.join(WORKDIR, 'etc')
    os.makedirs(etcdir)
    shutil.copy2(os.path.join(BUILD_SRCDIR, 'tests/src/hosts'), etcdir)

    AUG = hosts_update.init(WORKDIR)


def teardown():
    global WORKDIR
    cleanupdir(WORKDIR)


@with_setup(setup, teardown)
def test_ip_match():
    global AUG, IP_00, IP_1, WORKDIR

    assert hosts_update.ip_match(AUG, IP_00) != [], "IP = %s" % IP_00 + \
        "\n\n/etc/hosts:\n%s\n" % open('%s/etc/hosts' % WORKDIR).read()
    assert hosts_update.ip_match(AUG, IP_1) == [], open('%s/etc/hosts' % WORKDIR).read()


@with_setup(setup, teardown)
def test_ip_add_remove():
    global AUG, IP_0, FQDN_0, HOST_0

    hosts_update.ip_add(AUG, IP_0, FQDN_0, HOST_0)
    assert hosts_update.ip_match(AUG, IP_0) != []

    hosts_update.ip_remove(AUG, IP_0)
    assert hosts_update.ip_match(AUG, IP_0) == []


@with_setup(setup, teardown)
def test_ip_add__force():
    global AUG, IP_0, FQDN_0, HOST_0

    hosts_update.ip_add(AUG, IP_0, FQDN_0, HOST_0, True)
    hosts_update.ip_add(AUG, IP_0, FQDN_0, HOST_0, True)
    assert hosts_update.ip_match(AUG, IP_0) != []


@with_setup(setup, teardown)
def test_ip_remove__not_exist():
    global AUG, IP_1

    hosts_update.ip_remove(AUG, IP_1)
    assert hosts_update.ip_match(AUG, IP_1) == []


if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:

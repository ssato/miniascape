import glob
import nose
import os
import sys
import shutil
import tempfile

from nose.tools import with_setup, assert_raises

sys.path.append('../')
import hosts_update as hu


WORKDIR = None
AUG = None

IP_00 = '127.0.0.1'  # Must exists in /etc/hosts.

# "300.0.0.1" is invalid IP address for hosts and must not exist in /etc/hosts.
# Even if it's invalid, it is suitable for testing purpose.
IP_0 = '300.0.0.1'
IP_1 = '300.0.0.2'
FQDN_0 = 'test-1.example.com'
HOST_0 = 'test-1'


def setup():
    global WORKDIR, AUG

    WORKDIR = tempfile.mkdtemp(dir=os.curdir)
    etcdir = os.path.join(WORKDIR, 'etc')
    os.makedirs(etcdir)

    shutil.copy2('/etc/hosts', etcdir)

    AUG = hu.init(WORKDIR)


def teardown():
    global WORKDIR

    etcdir = "%s/etc" % WORKDIR

    [os.remove(f) for f in glob.glob("%s/*" % etcdir)]

    if os.path.exists(etcdir):
        os.rmdir(etcdir)

    if os.path.exists(WORKDIR):
        os.rmdir(WORKDIR)


@with_setup(setup, teardown)
def test_ip_match():
    global AUG, IP_00, IP_1, WORKDIR

    assert hu.ip_match(AUG, IP_00) != [], "IP = %s" % IP_00 + \
        "\n\n/etc/hosts:\n%s\n" % open('%s/etc/hosts' % WORKDIR).read()
    assert hu.ip_match(AUG, IP_1) == [], open('%s/etc/hosts' % WORKDIR).read()


@with_setup(setup, teardown)
def test_ip_add():
    global AUG, IP_0, FQDN_0, HOST_0

    hu.ip_add(AUG, IP_0, FQDN_0, HOST_0)
    assert hu.ip_match(AUG, IP_0) != []


@with_setup(setup, teardown)
def test_ip_add_force():
    global AUG, IP_0, FQDN_0, HOST_0

    hu.ip_add(AUG, IP_0, FQDN_0, HOST_0, True)
    hu.ip_add(AUG, IP_0, FQDN_0, HOST_0, True)
    assert hu.ip_match(AUG, IP_0) != []


@with_setup(setup, teardown)
def test_ip_remove_exist():
    global AUG, IP_0

    hu.ip_remove(AUG, IP_0)
    assert hu.ip_match(AUG, IP_0) == []


@with_setup(setup, teardown)
def test_ip_remove_not_exist():
    global AUG, IP_1

    hu.ip_remove(AUG, IP_1)
    assert hu.ip_match(AUG, IP_1) == []


if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:

import miniascape as m
import nose
import os
import sys
import tempfile

from miniascape.virt import *
from miniascape.utils import runcmd
from tests.globals import *



def setup_images():
    runcmd("qemu-img create -f qcow2 %s 1M" % TEST_DOMAIN_IMAGE_BASE_1)
    runcmd("qemu-img create -f qcow2 -b %s %s" % (TEST_DOMAIN_IMAGE_BASE_1, TEST_DOMAIN_IMAGE_1))
    runcmd("qemu-img create -f qcow2 %s 1M" % TEST_DOMAIN_IMAGE_BASE_2)
    runcmd("qemu-img create -f qcow2 -b %s %s" % (TEST_DOMAIN_IMAGE_BASE_2, TEST_DOMAIN_IMAGE_2))


def teardown_images():
    for img in (TEST_DOMAIN_IMAGE_1, TEST_DOMAIN_IMAGE_2, TEST_DOMAIN_IMAGE_BASE_1, TEST_DOMAIN_IMAGE_BASE_2):
        os.remove(img)


# tests:
def test_LibvirtObject_by_name():
    global TEST_DOMAIN_XML, TEST_CONFIG_FILE

    lo = LibvirtObject(xml_path=TEST_DOMAIN_XML, pkg_config_path=TEST_CONFIG_FILE)
    assert isinstance(lo, LibvirtObject)
    assert lo.name == 'rhel-5-generic-0', "name: %s vs. rhel-5-generic-0" % lo.name
    assert lo.xml_path == TEST_DOMAIN_XML, "xml_path: %s vs. %s" % (lo.xml_path, TEST_DOMAIN_XML)

    lo.is_libvirtd_running()


def test_LibvirtNetwork():
    global TEST_NETWORK_XML, TEST_CONFIG_FILE

    x = LibvirtNetwork(xml_path=TEST_NETWORK_XML, pkg_config_path=TEST_CONFIG_FILE)
    assert isinstance(x, LibvirtNetwork)
    assert x.name == 'net-1', "name: %s vs. net-1" % x.name
    assert x.xml_path == TEST_NETWORK_XML, "xml_path: %s vs. %s" % (x.xml_path, TEST_NETWORK_XML)


# TODO: How to test LibvirtDomain.{install,uninstall,is_running, ...}
@nose.tools.with_setup(setup_images, teardown_images)
def test_LibvirtDomain():
    global TEST_DOMAIN_XML, TEST_CONFIG_FILE, TEST_DOMAIN_IMAGE_1, TEST_DOMAIN_IMAGE_2, TEST_DOMAIN_IMAGE_BASE_1, TEST_DOMAIN_IMAGE_BASE_2

    x = LibvirtDomain(xml_path=TEST_DOMAIN_XML, pkg_config_path=TEST_CONFIG_FILE)
    assert isinstance(x, LibvirtDomain)
    assert x.name == 'rhel-5-generic-0', "name: %s vs. rhel-5-generic-0" % x.name
    assert x.xml_path == TEST_DOMAIN_XML, "xml_path: %s vs. %s" % (x.xml_path, TEST_DOMAIN_XML)

    x.parse()
    assert x.arch == 'i686', "arch: %s vs. i686" % x.arch

    ns0 = ['net-1', 'net-3']
    assert x.networks == ns0, "networks: %s vs. %s" % (str(x.networks), str(ns0))

    is0 = [TEST_DOMAIN_IMAGE_1, TEST_DOMAIN_IMAGE_2]
    ibs0 = [TEST_DOMAIN_IMAGE_BASE_1, TEST_DOMAIN_IMAGE_BASE_2]

    assert x.images == is0, "images: %s vs. %s" % (str(x.images), str(is0))
    assert x.base_images == ibs0, "base images: %s vs. %s" % (str(x.base_images), str(ibs0))


#@nose.tools.with_setup(teardown=teardown_mkdir)
#def test_mkdir(dir=TESTDIR_0):

if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:

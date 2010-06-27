import miniascape as m
import nose
import os
import sys
import tempfile

from miniascape.tools import *
from miniascape.utils import runcmd
from tests.globals import *



def setup_images():
    runcmd("qemu-img create -f qcow2 %s 1M" % TEST_DOMAIN_IMAGE_BASE_1)
    runcmd("cd %s && qemu-img create -f qcow2 -b %s %s" % (os.path.dirname(TEST_DOMAIN_IMAGE_BASE_1), TEST_DOMAIN_IMAGE_BASE_1, TEST_DOMAIN_IMAGE_1))
    

def teardown_images():
    for img in (TEST_DOMAIN_IMAGE_1, TEST_DOMAIN_IMAGE_BASE_1):
        os.remove(img)


# tests:
def test_is_libvirtd_running():
    is_libvirtd_running()


@nose.tools.with_setup(setup_images, teardown_images)
def test_create_delta_image():
    os.remove(TEST_DOMAIN_IMAGE_1)
    create_delta_image(TEST_DOMAIN_IMAGE_BASE_1, os.path.basename(TEST_DOMAIN_IMAGE_1))

    assert os.path.exists(TEST_DOMAIN_IMAGE_1)
    assert os.path.isfile(TEST_DOMAIN_IMAGE_1)
    assert base_image_path_for_delta_image_path(TEST_DOMAIN_IMAGE_1) == TEST_DOMAIN_IMAGE_BASE_1


@nose.tools.with_setup(setup_images, teardown_images)
def test_create_delta_image():
    assert base_image_path_for_delta_image_path(TEST_DOMAIN_IMAGE_1) == TEST_DOMAIN_IMAGE_BASE_1


if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:

import nose
import os
import sys

import miniascape

from miniascape.pack import *
from tests.globals import *



WORKDIR = 'workdir'



def setup():
    global WORKDIR

    #WORKDIR = tempfile.mkdtemp(dir=TESTDIR)
    WORKDIR = os.path.join(TESTDIR, "pack_test")
    if not os.path.exists(WORKDIR):
        os.makedirs(WORKDIR, 0700)


def teardown():
    global WORKDIR

    cleanupdir(WORKDIR)


def setup_images():
    global WORKDIR, TEST_DOMAIN_XML

    setup()

    assert os.path.exists(WORKDIR) and os.path.isdir(WORKDIR)

    delta_images = miniascape.utils.xpath_eval("//devices/disk[@type='file']/source/@file", TEST_DOMAIN_XML)

    base_images = [img.replace(".qcow2", "-base.qcow2") for img in delta_images]

    for img in base_images:
        miniascape.utils.runcmd("qemu-img create -f qcow2 %s 1M" % img)

        delta = os.path.basename(img.replace("-base", ""))
        miniascape.tools.create_delta_image(img, delta)



# tests:
def test_PackageDTO():
    pd = PackageDTO('foo', 'minimal', '0.1')

    assert pd.domain_name == 'foo'
    assert pd.variant == 'minimal'
    assert pd.name == 'vm-foo-minimal'
    assert pd.version == '0.1'
    assert pd.virtual_name == 'vm-foo'
    assert pd.provides == pd.virtual_name
    

def test_DomainDTO():
    vmn = 'rhel-5-5-vm-1'
    vmxml = "/etc/libvirt/qemu/%s.xml" % vmn
    vmxmlsp = "/etc/miniascape/domain.d/%s.xml" % vmn
    bis = [TEST_DOMAIN_IMAGE_BASE_1, TEST_DOMAIN_IMAGE_BASE_2]
    dis = [TEST_DOMAIN_IMAGE_1, TEST_DOMAIN_IMAGE_2]

    dd = DomainDTO(vmn, vmxml, vmxmlsp)

    assert dd.name == vmn
    assert dd.xml_path == vmxml
    assert dd.xml_store_path == vmxmlsp
    assert dd.base_images == []
    assert dd.delta_images == []

    dd.add_base_images(bis)
    assert dd.base_images[0].dir == os.path.dirname(TEST_DOMAIN_IMAGE_BASE_1)
    assert dd.base_images[1].dir == os.path.dirname(TEST_DOMAIN_IMAGE_BASE_2)
    assert dd.base_images[0].name == os.path.basename(TEST_DOMAIN_IMAGE_BASE_1)
    assert dd.base_images[1].name == os.path.basename(TEST_DOMAIN_IMAGE_BASE_2)

    dd.add_delta_images(dis)
    assert dd.delta_images[0].dir == os.path.dirname(TEST_DOMAIN_IMAGE_1)
    assert dd.delta_images[1].dir == os.path.dirname(TEST_DOMAIN_IMAGE_2)
    assert dd.delta_images[0].name == os.path.basename(TEST_DOMAIN_IMAGE_1)
    assert dd.delta_images[1].name == os.path.basename(TEST_DOMAIN_IMAGE_2)

    dd2 = DomainDTO(vmn, vmxml, vmxmlsp, bis, dis)

    assert dd.base_images[0].dir == os.path.dirname(TEST_DOMAIN_IMAGE_BASE_1)
    assert dd.base_images[1].dir == os.path.dirname(TEST_DOMAIN_IMAGE_BASE_2)
    assert dd.base_images[0].name == os.path.basename(TEST_DOMAIN_IMAGE_BASE_1)
    assert dd.base_images[1].name == os.path.basename(TEST_DOMAIN_IMAGE_BASE_2)
    assert dd.delta_images[0].dir == os.path.dirname(TEST_DOMAIN_IMAGE_1)
    assert dd.delta_images[1].dir == os.path.dirname(TEST_DOMAIN_IMAGE_2)
    assert dd.delta_images[0].name == os.path.basename(TEST_DOMAIN_IMAGE_1)
    assert dd.delta_images[1].name == os.path.basename(TEST_DOMAIN_IMAGE_2)


@nose.tools.with_setup(setup, teardown)
def test_BuildProcess():
    global WORKDIR, TESTDIR

    config_path = os.path.join(TESTDIR, 'config')

    name = 'rhel-5-5-vm-1'
    variant = 'minimal'
    version = '0.1'

    bp = BuildProcess(name, variant, version, topdir=WORKDIR, pkg_config_path=config_path)
    workdir0 = os.path.join(WORKDIR, "%s-%s" % (bp.package.name, bp.package.version))

    assert bp.workdir == workdir0, "bp.workdir=%s (expected=%s)" % (bp.workdir, workdir0)

    bp.setup()

    rpmmk = os.path.join(bp.workdir, 'rpm.mk')
    m4dir = os.path.join(bp.workdir, 'm4')

    assert os.path.exists(bp.workdir) and os.path.isdir(bp.workdir)
    assert os.path.exists(rpmmk) and os.path.isfile(rpmmk)
    assert os.path.exists(m4dir) and os.path.isdir(m4dir)


#@nose.tools.with_setup(setup_images, teardown)
@nose.tools.with_setup(setup_images)
def test_RepackProcess():
    global WORKDIR, TESTDIR, TEST_DOMAIN_XML

    config_path = os.path.join(TESTDIR, 'config')

    name = miniascape.utils.xpath_eval('/domain/name', TEST_DOMAIN_XML)[0]

    rp = RepackProcess(name, topdir=WORKDIR, pkg_config_path=config_path)

    rp.setup_domain_xml()
    xmlfile = os.path.join(rp.workdir, "%s.xml" % rp.domain.name)

    assert os.path.exists(xmlfile) and os.path.isfile(xmlfile)

    rp.setup_domain_images()


if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:

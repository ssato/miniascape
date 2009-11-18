import glob
import nose
import os
import re
import sys
import shutil
import tempfile

try:
    import xml.etree.ElementTree as ET  # python >= 2.5
except ImportError:
    import elementtree.ElementTree as ET  # python <= 2.4; needs ElementTree.

from nose.tools import with_setup

sys.path.append('../')
import repackage


WORKDIR = None
DOMNAME = 'rhel-5-4-guest-1'
BASE_IMG = 'base.img'
DELTA_IMG = 'delta.img'



def setup():
    global WORKDIR

    WORKDIR = tempfile.mkdtemp()


def image_setup():
    global WORKDIR, BASE_IMG, DELTA_IMG

    setup()
    os.system("cd %s && qemu-img create -f qcow2 %s 1M 2>&1 >/dev/null" % (WORKDIR, BASE_IMG))
    os.system("cd %s && qemu-img create -f qcow2 -b %s %s 2>&1 >/dev/null" % (WORKDIR, BASE_IMG, DELTA_IMG))


def teardown():
    global WORKDIR

    [os.remove(f) for f in glob.glob("%s/*" % WORKDIR)]

    if os.path.exists(WORKDIR):
        os.rmdir(WORKDIR)


try:
    all
except NameError:
    def all(xs):
        return [x for x in xs if not x] == []


# tests:

def test_run():
    cmds = 'ls /proc/sys/fs/file-nr'

    (ret, out) = repackage.run(cmds)

    assert ret == 0, "return code = %d" % ret
    assert out == cmds.split()[1]


def test_package_name():
    global DOMNAME

    assert "%s-%s-%s" % (repackage.RPMNAME_PREFIX, DOMNAME, repackage.RPMNAME_SUFFIX) \
        == repackage.package_name(DOMNAME, repackage.RPMNAME_PREFIX, repackage.RPMNAME_SUFFIX)


def test_is_libvirtd_running():
    is_root = False

    if is_root:
        repackage.run("/etc/rc.d/init.d/libvirtd restart")
        assert repackage.is_libvirtd_running()

        repackage.run("/etc/rc.d/init.d/libvirtd stop")
        assert not repackage.is_libvirtd_running()


## TODO:
def test_get_domain_xml():
    pass

def test_domain_image_paths():
    pass

def test_domain_status():
    pass

@with_setup(setup, teardown)
def test_substfile():
    global WORKDIR

    src = '%s/subst_src_0' % WORKDIR
    dst = src + '.new'

    open(src, 'w').write('aaa=bbb')
    repackage.substfile(src, dst, {'bbb': 'ccc'})

    assert re.match('aaa=bbb', open(src).read()) is not None
    assert re.match('aaa=bbb', open(dst).read()) is None
    assert re.match('aaa=ccc', open(dst).read()) is not None


@with_setup(setup, teardown)
def test_createdir():
    global WORKDIR

    dir = '%s/test-1' % WORKDIR
    repackage.createdir(dir)

    assert os.path.isdir(dir)

    os.rmdir(dir)


def test_parse_domain_xml():
    global DOMNAME

    domxml = "%s.xml" % DOMNAME
    content = open(domxml).read()

    dominfo = repackage.parse_domain_xml(content)
    name = DOMNAME
    arch = 'i686'
    images = sorted(["/var/lib/libvirt/images/%s-disk-1.qcow2" % DOMNAME, ])

    assert name == dominfo['name']
    assert arch == dominfo['arch']
    assert all([x == y for x, y in zip(images, dominfo['images'])])


@with_setup(image_setup, teardown)
def test_base_image_path():
    global WORKDIR, BASE_IMG, DELTA_IMG

    bpath = "%s/%s" % (WORKDIR, BASE_IMG)
    dpath = "%s/%s" % (WORKDIR, DELTA_IMG)
    path = repackage.base_image_path(dpath)
    print "***\npath = '%s'\n***\n" % path

    assert bpath == path, "delta = %s, base = %s, base = %s (result)" % (bpath, dpath, path)


@with_setup(image_setup, teardown)
def test_copyfile():
    global WORKDIR, BASE_IMG

    img = "%s/%s" % (WORKDIR, BASE_IMG)

    repackage.copyfile(img, img + ".copy")

    assert os.path.exists(img + ".copy")


if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:

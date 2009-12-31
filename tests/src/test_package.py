import nose
import os
import re

from nose.tools import with_setup

from globals import *
import package



WORKDIR = None

DOMNAME = 'test-domain-1'
DOMXML = DOMNAME + '.xml'

NORM_IMG_1 = 'test-domain-1-disk-1.qcow2'
DELTA_IMG_1 = 'test-domain-1-disk-2.qcow2'
DELTA_IMG_1_BASE = 'test-domain-1-disk-2-base.qcow2'

IMGS_IN_DOMXML = [os.path.join('@TESTDIR@', i) for i in (NORM_IMG_1, DELTA_IMG_1)]



def setup():
    global WORKDIR
    WORKDIR = setupdir()


def teardown():
    global WORKDIR
    prune_dir(WORKDIR)


def images_setup():
    global WORKDIR, TEST_IMAGES_DIR, DELTA_IMG_1, DELTA_IMG_1_BASE

    setup()

    TEST_IMAGES_DIR = os.path.join(WORKDIR, 'images')

    os.mkdir(TEST_IMAGES_DIR)
    runcmd("chcon -R -t virt_image_t %s" % TEST_IMAGES_DIR)

    create_image(TEST_IMAGES_DIR, NORM_IMG_1)
    create_delta_image(TEST_IMAGES_DIR, DELTA_IMG_1_BASE, DELTA_IMG_1)

    xmlcontent = open(DOMXML).read().replace('@TESTDIR@', TEST_IMAGES_DIR)
    open(os.path.join(TEST_IMAGES_DIR, DOMXML),'w').write(xmlcontent)


def build_setup():
    global WORKDIR, BUILD_SRCDIR, TEST_BUILD_DIR, DOMNAME, DOMXML

    images_setup()

    TEST_BUILD_DIR = os.path.join(WORKDIR, 'build_data')
    os.mkdir(TEST_BUILD_DIR)

    copytree(os.path.join(BUILD_SRCDIR, 'aux'), TEST_BUILD_DIR)
    copytree(os.path.join(BUILD_SRCDIR, 'data/package/'), TEST_BUILD_DIR)
    copytree(os.path.join(BUILD_SRCDIR, 'data/repackage/'), TEST_BUILD_DIR)


# tests:
def test_run():
    cmds = 'ls %s' % "test_package.py"

    (ret, out) = package.run(cmds)

    assert ret == 0, "return code = %d" % ret
    assert out == cmds.split()[1]


def test_package_name():
    global DOMNAME

    assert "%s-%s-%s" % (package.RPMNAME_PREFIX, DOMNAME, package.RPMNAME_SUFFIX) \
        == package.package_name(DOMNAME, package.RPMNAME_PREFIX, package.RPMNAME_SUFFIX)


def test_is_libvirtd_running():
    is_root = False

    if is_root:
        package.run("/etc/rc.d/init.d/libvirtd restart")
        assert package.is_libvirtd_running()

        package.run("/etc/rc.d/init.d/libvirtd stop")
        assert not package.is_libvirtd_running()


## TODO:
def test_get_domain_xml():
    pass

def test_domain_status():
    pass


@with_setup(setup, teardown)
def test_substfile():
    global WORKDIR

    src = os.path.join(WORKDIR, 'subst_src_0')
    dst = src + '.new'

    open(src, 'w').write('aaa=bbb')
    package.substfile(src, dst, {'bbb': 'ccc'})

    assert re.match('aaa=bbb', open(src).read()) is not None
    assert re.match('aaa=bbb', open(dst).read()) is None
    assert re.match('aaa=ccc', open(dst).read()) is not None


@with_setup(setup, teardown)
def test_createdir():
    global WORKDIR

    dir = os.path.join(WORKDIR, 'test-1')
    package.createdir(dir)

    assert os.path.isdir(dir)

    os.rmdir(dir)


def test_parse_domain_xml():
    global DOMNAME, DOMXML, IMGS_IN_DOMXML

    dominfo = package.parse_domain_xml(open(DOMXML).read())
    arch = 'i686'
    images = sorted(IMGS_IN_DOMXML)

    assert DOMNAME == dominfo['name']
    assert arch == dominfo['arch']
    assert all((x == y for x, y in zip(images, dominfo['images'])))


@with_setup(images_setup, teardown)
def test_base_image_path_normal_image():
    global TEST_IMAGES_DIR, NORM_IMG_1

    ipath = os.path.join(TEST_IMAGES_DIR, NORM_IMG_1)
    bpath = package.base_image_path(ipath)

    assert bpath == "", "image = '%s', base = '%s'" % (ipath, bpath)


@with_setup(images_setup, teardown)
def test_base_image_path_delta_image():
    global TEST_IMAGES_DIR, DELTA_IMG_1_BASE, DELTA_IMG_1 

    ipath = os.path.join(TEST_IMAGES_DIR, DELTA_IMG_1)
    bpath = package.base_image_path(ipath)

    assert bpath != "", "image = '%s', base = '%s'" % (ipath, bpath)
    assert bpath == os.path.join(TEST_IMAGES_DIR, DELTA_IMG_1_BASE), \
        "image = '%s', base = '%s'" % (ipath, bpath)


@with_setup(images_setup, teardown)
def test_domain_image_paths():
    global TEST_IMAGES_DIR, DOMXML, IMGS_IN_DOMXML, DELTA_IMG_1_BASE

    domxml_content = open(os.path.join(TEST_IMAGES_DIR, DOMXML)).read()
    ref_images = sorted(
        [p.replace('@TESTDIR@', TEST_IMAGES_DIR) for p in IMGS_IN_DOMXML] + \
            [os.path.join(TEST_IMAGES_DIR, DELTA_IMG_1_BASE)]
    )

    images = sorted(package.domain_image_paths(domxml_content))

    assert all((x == y for x, y in zip(images, ref_images))), \
        "images = '%s', ref_images = '%s'" % (str(images),str(ref_images))


@with_setup(setup, teardown)
def test_copyfile():
    global WORKDIR, DOMXML

    copyto = os.path.join(WORKDIR, DOMXML + '.copy')
    package.copyfile(DOMXML, copyto)

    assert os.path.exists(copyto)


@with_setup(build_setup, teardown)
def test_do_repackage_setup():
    global WORKDIR, BUILD_SRCDIR, BUILD_DATADIR, TEST_BUILD_DIR, DOMXML, DOMNAME

    builddir = package.make_builddir(WORKDIR, DOMNAME)
    domxml = os.path.join(TEST_IMAGES_DIR, DOMXML)
    package.do_repackage_setup(TEST_BUILD_DIR, DOMNAME, 'minimal', domxml, builddir)


@with_setup(build_setup, teardown)
def test_do_build__repackage():
    global WORKDIR, BUILD_SRCDIR, BUILD_DATADIR, TEST_BUILD_DIR, DOMXML, DOMNAME

    builddir = package.make_builddir(WORKDIR, DOMNAME)
    domxml = os.path.join(TEST_IMAGES_DIR, DOMXML)
    package.do_repackage_setup(TEST_BUILD_DIR, DOMNAME, 'minimal', domxml, builddir)
    package.do_build(DOMNAME, builddir)


#@with_setup(build_setup, teardown)
@with_setup(build_setup)
def test_do_package__repackage():
    global WORKDIR, BUILD_SRCDIR, BUILD_DATADIR, TEST_BUILD_DIR, DOMXML, DOMNAME

    builddir = package.make_builddir(WORKDIR, DOMNAME)
    domxml = os.path.join(TEST_IMAGES_DIR, DOMXML)
    package.do_repackage_setup(TEST_BUILD_DIR, DOMNAME, 'minimal', domxml, builddir)
    package.do_build(DOMNAME, builddir)
    package.do_package(DOMNAME, builddir)


@with_setup(build_setup, teardown)
def test_do_package_setup():
    global WORKDIR, TEST_BUILD_DIR, DOMXML, DOMNAME

    builddir = package.make_builddir(WORKDIR, DOMNAME)
    package.do_package_setup(TEST_BUILD_DIR, DOMNAME, 'minimal', builddir)


if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:

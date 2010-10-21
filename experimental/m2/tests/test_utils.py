import nose
import os
import sys
import tempfile

from miniascape.utils import *
from tests.globals import *



XMLFILE_0 = 'test0.xml'
XMLCONTENT_0 = "<a><b><c d='xyz'/></b><e>abc</e><e>def</e></a>"

TESTDIR_0 = './testdir0'

TESTSRC_0 = None
TESTDST_0 = None

KEYFILE_0 = 'keyfile_0.key'



def setup_xmlfile(xmlfile=XMLFILE_0, xmlcontent=XMLCONTENT_0):
    open(xmlfile, 'w').write(xmlcontent)


def teardown_xmlfile(xmlfile=XMLFILE_0):
    os.remove(xmlfile)


def teardown_mkdir(dir=TESTDIR_0):
    os.removedirs(dir)


def setup_copyfile():
    global TESTSRC_0, TESTDST_0

    (_fd, TESTSRC_0) = tempfile.mkstemp(dir='./')
    TESTDST_0 = TESTSRC_0 + '.dst'


def teardown_keyfile(keyfile=KEYFILE_0):
    os.remove(keyfile)


def teardown_copyfile():
    global TESTSRC_0, TESTDST_0
    os.remove(TESTSRC_0)
    os.remove(TESTDST_0)



# tests:
def test_FakeXattr():
    xattr = FakeXattr()
    xattr.get_all()
    xattr.set('test', 'xyz')


def test_memoize():
    @memoize
    def fib(n):
        if n < 2:
            return 1
        else:
            return fib(n-1) + fib(n-2)

    ret = fib(300)
    assert ret == 359579325206583560961765665172189099052367214309267232255589801L, ret


def test_unique():
    assert unique([]) == []
    assert unique([1]) == [1]
    assert unique(['a','b','c','b','a']) == ['a','b','c']
    assert unique([0, 3, 1, 2, 1, 0, 4, 5]) == [0, 1, 2, 3, 4, 5]


@nose.tools.with_setup(setup_xmlfile, teardown_xmlfile)
def test_xpath_eval():
    global XMLFILE_0
    xf = XMLFILE_0

    r0 = ['abcdef']
    r1 = ['abc', 'def']
    r2 = ['xyz']

    c0 = xpath_eval('/a', xf)
    c1 = xpath_eval('/a/e', xf)
    c2 = xpath_eval('//e', xf)
    c3 = xpath_eval('/a/b/c/@d', xf)

    assert c0 == r0, "%s (expected %s" % (str(c0), str(r0))
    assert c1 == r1, "%s (expected %s" % (str(c1), str(r1))
    assert c2 == r1, "%s (expected %s" % (str(c2), str(r1))
    assert c3 == r2, "%s (expected %s" % (str(c3), str(r2))



def test_kickstart_password():
    kp = kickstart_password('password')
    assert isinstance(kp, str)


def test_compile_template():
    global TEST_VIRTINST_TEMPLATE, TEST_VIRTINST_PARAMS, TEST_VIRTINST_OUT

    compile_template(TEST_VIRTINST_TEMPLATE, 'test.out', TEST_VIRTINST_PARAMS)
    c0 = open('test.out').read()

    c1 = open(TEST_VIRTINST_OUT).read()

    assert c0 == c1, "c0=%s, c1=%s" % (c0, c1)


def test_runcmd():
    (rc, out) = runcmd('echo "XYZ"')

    assert rc == 0, "rc=%d" % rc
    assert out == "XYZ", "out=%s" % out


@nose.tools.with_setup(teardown=teardown_mkdir)
def test_mkdir(dir=TESTDIR_0):
    mkdir(dir)

    assert os.path.exists(dir)
    assert os.path.isdir(dir)


def test_load_config():
    global NET_1_YAML

    load_config(NET_1_YAML)


@nose.tools.with_setup(teardown=teardown_keyfile)
def test_gen_fence_key(keyfile=KEYFILE_0):
    assert not os.path.exists(keyfile)

    gen_fence_key(keyfile)

    assert os.path.exists(keyfile)
    assert os.path.isfile(keyfile)


@nose.tools.with_setup(setup_copyfile, teardown_copyfile)
def test_copyfile():
    global TESTSRC_0, TESTDST_0

    src = TESTSRC_0
    dst = TESTDST_0

    assert not os.path.exists(dst)

    copyfile(TESTSRC_0, TESTDST_0)

    assert os.path.exists(dst)
    assert os.path.isfile(dst)

    copyfile(src, dst, True)

    assert os.path.exists(dst)
    assert os.path.isfile(dst)


if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:

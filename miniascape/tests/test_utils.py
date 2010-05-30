import nose
import os
import sys

from miniascape.utils import *
from tests.globals import *



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


def test_kickstart_password():
    kp = kickstart_password('password')
    assert isinstance(kp, str)


def test_compile_template():
    global TEST_VIRTINST_TEMPLATE, TEST_VIRTINST_PARAMS, TEST_VIRTINST_OUT

    c0 = compile_template(TEST_VIRTINST_TEMPLATE, TEST_VIRTINST_PARAMS)
    c1 = open(TEST_VIRTINST_OUT).read()

    assert c0 == c1, "c0=%s, c1=%s" % (c0, c1)


def test_runcmd():
    (rc, out) = runcmd('echo "XYZ"')

    assert rc == 0, "rc=%d" % rc
    assert out == "XYZ", "out=%s" % out


if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:

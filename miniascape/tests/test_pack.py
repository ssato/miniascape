import nose
import os
import sys

from miniascape.pack import *
from miniascape.utils import runcmd
from tests.globals import *



# tests:
def test_PackageDTO():
    pd = PackageDTO('foo', 'minimal', '0.1')

    assert pd.domain_name == 'foo'
    assert pd.variant == 'minimal'
    assert pd.name == 'vm-foo-minimal'
    assert pd.version == '0.1'
    assert pd.virtual_name == 'vm-foo'
    assert pd.provides == pd.virtual_name
    


if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:

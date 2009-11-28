import glob
import nose
import os
import sys
import shutil
import tempfile

try:
    import xml.etree.ElementTree as ET  # python >= 2.5
except ImportError:
    import elementtree.ElementTree as ET  # python <= 2.4; needs ElementTree.

from nose.tools import with_setup

sys.path.append('../')
import netxml_del_dhcp as ndd


WORKDIR = None

NETXML_SRC = '../../data/libvirt/net-1.xml.in.in'
NETXML_0 = None


def setup():
    global WORKDIR, NETXML_SRC, NETXML_0

    WORKDIR = tempfile.mkdtemp(dir=os.curdir)
    shutil.copy2(NETXML_SRC, WORKDIR)

    NETXML_0 = os.path.join(WORKDIR, os.path.basename(NETXML_SRC))


def teardown():
    global WORKDIR

    [os.remove(f) for f in glob.glob("%s/*" % WORKDIR)]

    if os.path.exists(WORKDIR):
        os.rmdir(WORKDIR)


def path_not_exist(xml, path):
    tree = ET.parse(xml)
    found = tree.find(path)

    return found is None


@with_setup(setup, teardown)
def test_delete_dhcp_stuff():
    global NETXML_0

    netxml = NETXML_0
    output = NETXML_0 + '.new'

    ndd.delete_dhcp_stuff(netxml, output)

    assert path_not_exist(output, 'ip/dhcp')


if __name__ == '__main__':
    nose.runmodule()

# vim: set sw=4 ts=4 et:
